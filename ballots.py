import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import outputs


def read_file(file_address):
    ballot_file = open(file_address, "r")
    lines = ballot_file.readlines()
    # Remove num candidates and votes per ballot
    first_line = lines[0].split(' ')
    lines.remove(lines[0])
    lines.remove(lines[1])
    lines.remove(lines[-1])
    return lines, int(first_line[0]), int(first_line[1])


def get_ballots_and_candidates(file_address):
    """Get ballots and candidates as lists"""
    lines, num_candidates, num_seats = read_file(file_address)

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

    # Remove title
#    candidates.remove(candidates[-1])
    return ballots, candidates, num_candidates, num_seats


def get_slate_keys(slate, candidates):
    candidate_names = list(candidates.values())
    return [[candidate_names.index(candidate) for candidate in slate[0]]]


def transform_matrix(ballots, num_candidates):
    """Transform ballots into 'rank' matrices. The first candidate voted for by a voter gets rank 44.
    The last gets 1. Anyone not voted for gets 0"""
    transformed_ballots = [[0] * num_candidates for i in range(len(ballots))]

    for ballot_num in range(len(ballots)):
        ballot = ballots[ballot_num]
        value = num_candidates
        for vote_num in range(len(ballot)):
            transformed_ballots[ballot_num][ballot[vote_num] - 1] = value
            value -= 1

    return transformed_ballots


def do_pca(transformed_ballots):
    array = np.array(transformed_ballots)
    pca = PCA(n_components=15)
    reduced_array = pca.fit_transform(array)
    return reduced_array, pca


def pick_number_nodes():
    cluster_variances = []
    cluster_choices = range(1, 10)

    for i in cluster_choices:
        kmeans_model = KMeans(n_clusters=i, n_init=100).fit(reduced_array)
        cluster_variances.append(
            100 - sum(np.min(cdist(reduced_array, kmeans_model.cluster_centers_, 'euclidean'), axis=1)) /
            reduced_array.shape[0])

    plt.plot(cluster_choices, cluster_variances, 'bx-')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Variance Explained')
    plt.title('The Elbow Method showing the optimal k')
    plt.savefig('output_files/2021/node_numbers.png')


def split_clusters(reduced_array, cluster_labels):

    indices1 = [i for i, x in enumerate(cluster_labels) if x == 0]
    indices2 = [i for i, x in enumerate(cluster_labels) if x == 1]
    indices3 = [i for i, x in enumerate(cluster_labels) if x == 2]
    indices4 = [i for i, x in enumerate(cluster_labels) if x == 3]
    indices5 = [i for i, x in enumerate(cluster_labels) if x == 4]
    #indices6 = [i for i, x in enumerate(cluster_labels) if x == 5]

    return [[list(reduced_array[i]) for i in indices1], [list(reduced_array[i]) for i in indices2], [list(reduced_array[i]) for i in indices3], [list(reduced_array[i]) for i in indices4], [list(reduced_array[i]) for i in indices5]]#, [list(reduced_array[i]) for i in indices6]]


def get_vote_counts_for_candidate(ballots, num_candidates):
    counts = np.zeros((num_candidates, num_candidates + 1), dtype=np.int8)
    for i in range(num_candidates):
        votes_for_candidate = ballots[:, int(i)]
        for vote in votes_for_candidate:
            counts[i][vote] += 1

    return counts


def get_clustered_vote_counts(clusters, num_candidates):
    return [get_vote_counts_for_candidate(np.array(cluster), num_candidates) for cluster in clusters]


def vote_counts(vote_cast, counts, ballots, ballot_index, i, max_value):
    return len(ballots[ballot_index]) > i and np.array(counts[ballots[ballot_index][i] - 1]).sum() < max_value and not vote_cast[ballot_index]


def get_cluster_counts(cluster_labels):
    cluster_counts = [0, 0, 0, 0, 0, 0]

    for cluster in cluster_labels:
        cluster_counts[cluster] += 1

    return cluster_counts


## 2019 slates
# momentum_slate = [[11, 44, 18, 15, 47, 39, 13, 31, 34, 8, 5, 38, 37, 2, 4, 26, 46, 43, 19, 32, 48, 6, 7, 25, 21, 3, 33, 50, 16, 17]]
# left_unity_slate_dep = [[27, 14, 12, 24, 23, 30, 20, 49, 42, 35, 41, 51]]
# left_unity_slate = [[24, 12, 23, 30, 27, 14, 20, 28, 49, 35, 42, 41, 51, 36, 9, 1, 29, 40]]

## 2021 slates
lu_slate = [['Anlin Wang', 'Sal H', 'Julia Alekseyeva', 'Meag Jae Kaman', 'Ron Joseph', 'Austin Binns', 'Melissa Duvelsdorf',
                     'Aliyah Bixby-Driesen', 'Michele Rossi', 'Shawn Hogan', 'Sanwal Yousaf', 'Emily Berkowitz', 'Matt Chewning',
                     'Francisco Diez', 'Will M', 'Matthew Zanowic', 'Mike Dewar', 'Sam Layding', 'Patrick Wargo', 'Daisy Confoy', 'Rebecca Johnson']]
br_slate = [['Bill Bradley', 'John Campbell', 'Amanda Fox', 'Dave Fox', 'Ethan Hill', 'K.T. Liberato']]
number_clusters = 6

ballots, candidates, num_candidates, num_seats = get_ballots_and_candidates("include/2021ballots.txt")

lu_slate_keys = get_slate_keys(lu_slate, candidates)
br_slate_keys = get_slate_keys(br_slate, candidates)

transformed_ballots = transform_matrix(ballots, num_candidates)
reduced_array, pca = do_pca(transformed_ballots)

cluster_labels = KMeans(n_clusters=number_clusters, n_init=100).fit_predict(reduced_array)

transformed_br = transform_matrix(br_slate_keys, num_candidates)
rotated_br = pca.transform(transformed_br)

transformed_lu = transform_matrix(lu_slate_keys, num_candidates)
rotated_lu = pca.transform(transformed_lu)

rotated_slates = np.array([rotated_br[0], rotated_lu[0]])

clusters = split_clusters(reduced_array, cluster_labels)
vote_clusters = split_clusters(transformed_ballots, cluster_labels)
cluster_counts = get_cluster_counts(cluster_labels)

#outputs.plot_pca_ballots(np.array(cluster1), np.array(cluster2), np.array(cluster3), np.array(cluster4), np.array(cluster5), np.array(cluster6), rotated_slates)
#outputs.print_totals(pca, cluster_counts)

votes = get_clustered_vote_counts(np.array(vote_clusters), num_candidates)
#print(votes1)
outputs.plot_vote_counts(votes, candidates)

#outputs.print_slates(candidates, momentum_slate, left_unity_slate)

#outputs.print_important_components(pca, candidates)
#outputs.plot_important_components(pca, candidates)
