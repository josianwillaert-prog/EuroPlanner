from collections import defaultdict

from models.diagram import Diagram
from services.diagram_locator import DiagramLocator
from services.pdf_layout_reader import PageWord


class DiagramFactory:
    def __init__(self, locator: DiagramLocator | None = None):
        self.locator = locator or DiagramLocator()

    def create_diagrams(self, mots: list[PageWord]) -> list[Diagram]:
        locations = self.locator.locate(mots)
        if not locations:
            return []

        mots_by_page = self._group_by_page(mots)
        locations_by_page = self._group_locations_by_page(locations)

        diagrams: list[Diagram] = []

        for page, page_locations in locations_by_page.items():
            page_words = mots_by_page.get(page, [])
            columns = self._split_locations_into_columns(page_locations)

            for x_min, x_max, column_locations in columns:
                column_words = [
                    word
                    for word in page_words
                    if x_min <= (word.x0 + word.x1) / 2 < x_max
                ]

                for index, location in enumerate(column_locations):
                    if len(column_locations) == 1:
                        start_top = location.top
                        end_top = float("inf")
                    elif index == 0:
                        next_location = column_locations[index + 1]
                        start_top = location.top
                        end_top = (location.bottom + next_location.top) / 2
                    elif index == len(column_locations) - 1:
                        previous_location = column_locations[index - 1]
                        start_top = (previous_location.bottom + location.top) / 2
                        end_top = float("inf")
                    else:
                        previous_location = column_locations[index - 1]
                        next_location = column_locations[index + 1]
                        start_top = (previous_location.bottom + location.top) / 2
                        end_top = (location.bottom + next_location.top) / 2

                    diagram_words = tuple(
                        word
                        for word in column_words
                        if start_top <= word.top < end_top
                    )

                    if diagram_words:
                        diagrams.append(
                            Diagram(
                                code=location.code,
                                page=page,
                                mots=diagram_words,
                            )
                        )

        return diagrams

    @staticmethod
    def _group_by_page(mots: list[PageWord]) -> dict[int, list[PageWord]]:
        pages: dict[int, list[PageWord]] = defaultdict(list)

        for mot in sorted(mots, key=lambda word: (word.page, word.top, word.x0)):
            pages[mot.page].append(mot)

        return pages

    @staticmethod
    def _group_locations_by_page(locations) -> dict[int, list]:
        pages: dict[int, list] = defaultdict(list)

        for location in locations:
            pages[location.page].append(location)

        return pages

    @staticmethod
    def _split_locations_into_columns(page_locations: list) -> list:
        locations = sorted(
            page_locations,
            key=lambda location: (location.x0 + location.x1) / 2,
        )

        if len(locations) == 1:
            return [(-float("inf"), float("inf"), sorted(locations, key=lambda l: (l.top, l.x0)))]

        clusters: list[list] = [[locations[0]]]
        last_center = (locations[0].x0 + locations[0].x1) / 2
        column_gap_threshold = 40.0

        for location in locations[1:]:
            center = (location.x0 + location.x1) / 2
            if center - last_center > column_gap_threshold:
                clusters.append([location])
            else:
                clusters[-1].append(location)
            last_center = center

        columns: list[tuple[float, float, list]] = []
        cluster_centers = [
            sum((loc.x0 + loc.x1) / 2 for loc in cluster) / len(cluster)
            for cluster in clusters
        ]

        start = -float("inf")
        for boundary, cluster in zip(
            [
                (cluster_centers[i] + cluster_centers[i + 1]) / 2
                for i in range(len(cluster_centers) - 1)
            ],
            clusters,
        ):
            columns.append(
                (
                    start,
                    boundary,
                    sorted(cluster, key=lambda l: (l.top, l.x0)),
                )
            )
            start = boundary

        columns.append(
            (
                start,
                float("inf"),
                sorted(clusters[-1], key=lambda l: (l.top, l.x0)),
            )
        )

        return columns

