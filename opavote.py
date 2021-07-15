import numpy as np
import os
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import outputs


class OpaVote:

    def __init__(self, ballot_location, output_location):
        self.ballot_location = ballot_location
        self.output_location = output_location

        self.ballots, self.candidates, self.num_candidates, self.num_seats = self.__read_ballots_and_candidates(ballot_location)
        self.vectorized_ballots = self.__vectorize_matrix(self.ballots, self.num_candidates)
        self.pca_ballots, self.pca = self.__do_pca(self.vectorized_ballots)

        self.num_clusters = 0
        self.cluster_labels = np.empty(1)
        self.cluster_centers = np.empty(1)

    def __read_ballots_and_candidates(self, file_address):
        """Get ballots and candidates as lists"""
        lines, num_candidates, num_seats = self.__read_ballot_file(file_address)

        ballots = [[0] * num_candidates for i in range(332)]
        candidates = {}
        is_ballot = True
        ballot_num = 0
        for ballot in lines:
            if ballot == '0\n':
                is_ballot = False
                continue

            if is_ballot:
                ballot = ballot.replace('\n', '')
                votes = [int(i) for i in ballot.split(' ')][1:-1]
                if votes:
                    ballots[ballot_num] = votes
                    ballot_num += 1
            else:
                candidate = ballot.replace('"', '').replace('\n', '')
                candidates[len(candidates)] = candidate

        return ballots, candidates, num_candidates, num_seats

    def __read_ballot_file(self, file_address):
        ballot_file = open(file_address, "r")
        lines = ballot_file.readlines()
        # Remove num candidates and votes per ballot
        first_line = lines[0].split(' ')
        lines.remove(lines[0])
        lines.remove(lines[1])
        lines.remove(lines[-1])
        return lines, int(first_line[0]), int(first_line[1])

    def __vectorize_matrix(self, ballots, num_candidates):
        """Transform ballots into 'rank' matrices. The first candidate voted for by a voter gets rank 44.
        The last gets 1. Anyone not voted for gets 0"""
        vectorized_ballots = [[0] * num_candidates for i in range(len(ballots))]

        for ballot_num in range(len(ballots)):
            ballot = ballots[ballot_num]
            value = num_candidates
            for vote_num in range(len(ballot)):
                vectorized_ballots[ballot_num][ballot[vote_num] - 1] = value
                value -= 1

        return vectorized_ballots

    def __do_pca(self, vectorized_ballots, num_components=15):
        pca = PCA(n_components=num_components)
        pca_ballots = pca.fit_transform(np.array(vectorized_ballots))
        return pca_ballots, pca

    def __get_slate_keys(self, slate):
        candidate_names = list(self.candidates.values())
        return [[candidate_names.index(candidate) + 1 for candidate in slate[0]]]

    def transform_slates(self, slates):
        """Vectorize and perform PCA on slates"""
        transformed_slates = np.empty(len(slates))

        for i in range(len(slates)):
            slate_keys = self.__get_slate_keys(slates[i])
            vectorized_br_slate = self.__vectorize_matrix(slate_keys, self.num_candidates)
            rotated_slate = self.pca.transform(vectorized_br_slate)
            transformed_slates[i] = rotated_slate[0]

        return transformed_slates

    def write_pca_variances(self):
        """Write text file with PCA components and percent variance explained for each"""
        outputs.write_pca_variances(self.pca, self.output_location)

    def write_pca_components_by_candidate(self):
        """Write text files with new PCA axes and each components representation on that axis"""
        outputs.write_pca_components_by_candidate(self.pca, self.candidates, self.output_location)

    def plot_important_pca_components(self, threshold=.16):
        """Plot the most important axes of the import PCA components"""
        outputs.plot_important_pca_components(self.pca, self.candidates, threshold, self.output_location)

    def generate_clusters(self, num_clusters):
        """Generate clusters using passed in number and save the labels and centers"""
        kmeans = KMeans(n_clusters=num_clusters, n_init=100)
        cluster_labels = kmeans.fit_predict(self.pca_ballots)

        np.save(self.output_location + "clusters/labels.npy", cluster_labels)
        np.save(self.output_location + "clusters/centers.npy", kmeans.cluster_centers_)

        self.cluster_centers = kmeans.cluster_centers_
        self.cluster_labels = cluster_labels

    def load_clusters(self):
        """Load in saved clusters"""
        self.cluster_labels = np.load(self.output_location + "clusters/labels.npy")
        self.cluster_centers = np.load(self.output_location + "clusters/centers.npy")

    def write_cluster_centers(self, cluster_names):
        """Write text file with pre-PCA location of cluster centers"""
        outputs.write_cluster_centers(self.pca.inverse_transform(self.cluster_centers), self.candidates, cluster_names, self.output_location)

    def write_diff_cluster_centers(self, cluster_names, compared_clusters):
        """Subtract one cluster location from another and write to text file so clusters can be compared"""
        reverted_clusters = self.pca.inverse_transform(self.cluster_centers)
        outputs.write_diff_cluster_centers(reverted_clusters, self.candidates, cluster_names, compared_clusters, self.output_location)

    def plot_cluster_number_variances(self):
        """Plot graph of explained variance vs number of nodes"""
        cluster_variances = []
        cluster_choices = range(1, 10)

        for i in cluster_choices:
            KMeans_model = KMeans(n_clusters=i, n_init=100).fit(self.pca_ballots)
            cluster_variances.append(
                100 - sum(np.min(cdist(self.pca_ballots, KMeans_model.cluster_centers_, 'euclidean'), axis=1)) /
                self.pca_ballots.shape[0])

        outputs.plot_cluster_number_variances(cluster_choices, cluster_variances, self.output_location)

    def __split_by_cluster(self, ballots):
        """Split ballots into separate indices in an array"""
        clusters = []
        for i in range(len(self.cluster_centers)):
            index = [j for j, x in enumerate(self.cluster_labels) if x == i]
            clustered_votes = np.array([list(ballots[j]) for j in index])
            clusters.append(clustered_votes)

        return clusters

    def __get_cluster_counts(self):
        """Get number of members in each cluster"""
        cluster_counts = [0] * len(self.cluster_centers)

        for cluster in self.cluster_labels:
            cluster_counts[cluster] += 1

        return cluster_counts

    def plot_ballots_pca(self, pca_slates, cluster_names, x_pca_index, y_pca_index, x_pca_description, y_pca_description):
        """Create 2 dimensional plots using the selected PCA components. Clusters are color-coded."""
        clustered_pca_ballots = self.__split_by_cluster(self.pca_ballots)
        outputs.plot_ballots_pca(np.array(clustered_pca_ballots), pca_slates, cluster_names, x_pca_index, y_pca_index, x_pca_description, y_pca_description, self.output_location)

    def write_cluster_counts(self, cluster_names):
        """Write text file with names of clusters and number of members."""
        cluster_counts = self.__get_cluster_counts()
        outputs.write_cluster_counts(cluster_counts, cluster_names, self.output_location)

    def plot_candidate_vote_distributions(self, cluster_names):
        """Calculate the number of votes for each candidate at each position and plot the distribution"""
        clustered_ballots = self.__split_by_cluster(self.vectorized_ballots)
        clustered_vote_counts = self.__get_clustered_vote_counts(np.array(clustered_ballots))
        outputs.plot_candidate_vote_distributions(clustered_vote_counts, self.candidates, cluster_names, self.output_location)

    def __get_clustered_vote_counts(self, clustered_ballots):
        """Count the number of votes in each position for each candidate by the clustered ballots passed in.
        Returns an array of clustered counts"""

        return [self.__count_cluster_votes_for_candidate(np.array(ballots_in_cluster)) for ballots_in_cluster in clustered_ballots]

    def __count_cluster_votes_for_candidate(self, ballots_in_cluster, ):
        """Count the number of votes in each position for each candidate by the cluster of ballots passed in."""

        counts = np.zeros((self.num_candidates, self.num_candidates + 1), dtype=np.int8)
        for i in range(self.num_candidates):
            votes_for_candidate = ballots_in_cluster[:, int(i)]
            for vote in votes_for_candidate:
                counts[i][vote] += 1

        return counts

    def query_ballots(self, query, cluster_names):
        """Write text file with all ballots with candidates at the specified voting positions"""
        outputs.ballot_query(query, self.ballots, self.cluster_labels, cluster_names, self.candidates, self.output_location)

