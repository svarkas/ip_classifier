from libs.node import Node

class RTtree:

    def rt_tree(self):
        legit_human = Node(label="LEGIT_HUMAN")
        malicious_crawler = Node(label="MALICIOUS_CRAWLER")

        doi_check = Node(
            feature="doi_variance",
            threshold=5,
            left=legit_human,
            right=malicious_crawler
        )
        assets_check = Node(
            feature="assets_ratio",
            threshold=0.2,
            left=doi_check,
            right=legit_human
        )
        root = Node(
            feature="time_entropy",
            threshold=0.5,
            left=assets_check,
            right=legit_human
        )

        return root
