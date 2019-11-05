import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import outputs


def read_file(file_address):
    ballot_file = open(file_address, "r")
    lines = ballot_file.readlines()
    # Remove num candidates and votes per ballot
    lines.remove(lines[0])
    return lines


def get_ballots_and_candidates(file_address, num_votes):
    """Get ballots and candidates as lists"""
    lines = read_file(file_address)

    ballots = [[0] * num_votes for i in range(333)]
    candidates = []
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
            candidates.insert(len(candidates), candidate)

    # Remove title
    candidates.remove(candidates[-1])
    return ballots, candidates


def transform_matrix(ballots, num_candidates):
    """Transform ballots into 'rank' matrices. The first candidate voted for by a voter gets rank 25.
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


def split_clusters(reduced_array, cluster_labels):
    indices1 = [i for i, x in enumerate(cluster_labels) if x == 0]
    indices2 = [i for i, x in enumerate(cluster_labels) if x == 1]
    indices3 = [i for i, x in enumerate(cluster_labels) if x == 2]

    return [list(reduced_array[i]) for i in indices1], [list(reduced_array[i]) for i in indices2], [list(reduced_array[i]) for i in indices3]


def get_vote_counts_for_candidate(ballots, num_candidates, num_votes):
    counts = np.zeros((num_candidates, num_votes + 1), dtype=np.int8)
    for i in range(num_candidates):
        votes_for_candidate = ballots[:, i:i + 1]
        for vote in votes_for_candidate:
            counts[i][vote[0]] += 1

    return counts


def get_clustered_vote_counts(cluster1, cluster2, cluster3, num_candidates, num_votes):
    votes1 = get_vote_counts_for_candidate(cluster1, num_candidates, num_votes)
    votes2 = get_vote_counts_for_candidate(cluster2, num_candidates, num_votes)
    votes3 = get_vote_counts_for_candidate(cluster3, num_candidates, num_votes)

    return votes1, votes2, votes3


def vote_counts(vote_cast, counts, ballots, ballot_index, i, max_value):
    return len(ballots[ballot_index]) > i and np.array(counts[ballots[ballot_index][i] - 1]).sum() < max_value and not vote_cast[ballot_index]


def run_stv(ballots, clusters, num_votes, num_candidates):
    max_value = len(ballots)/num_candidates
    counts = np.zeros((num_candidates, 3))
    win_order = np.zeros(num_candidates)
    vote_cast = [False for i in range(len(ballots))]
    for round in range(num_votes):
        for ballot_index in range(len(ballots)):
            if vote_counts(vote_cast, counts, ballots, ballot_index, round, max_value):
                candidate_index = ballots[ballot_index][round] - 1
                counts[candidate_index][clusters[ballot_index]] += 1
                votes_received = np.array(counts[candidate_index]).sum()
                if votes_received < max_value and win_order[candidate_index] == 0:
                    win_order[candidate_index] = int(round) + 1
                vote_cast[ballot_index] = True

    return counts, win_order


momentum_slate = [[11, 44, 18, 15, 47, 39, 13, 31, 34, 8, 5, 38, 37, 2, 4, 26, 46, 43, 19, 32, 48, 6, 7, 25, 21, 3, 33, 50, 16, 17]]
left_unity_slate_dep = [[27, 14, 12, 24, 23, 30, 20, 49, 42, 35, 41, 51]]
left_unity_slate = [[24, 12, 23, 30, 27, 14, 20, 28, 49, 35, 42, 41, 51, 36, 9, 1, 29, 40]]

num_candidates = 51

ballots, candidates = get_ballots_and_candidates("./include/ballots10 (1).txt", num_candidates)
transformed_ballots = transform_matrix(ballots, num_candidates)
print(transformed_ballots)



reduced_array, pca = do_pca(transformed_ballots)
cluster_labels = KMeans(n_clusters=3, n_init=100).fit_predict(reduced_array)

transformed_momentum = transform_matrix(momentum_slate, num_candidates)
rotated_momentum = pca.transform(transformed_momentum)

transformed_left_unity = transform_matrix(left_unity_slate, num_candidates)
rotated_left_unity = pca.transform(transformed_left_unity)

rotated_slates = np.array([rotated_momentum[0], rotated_left_unity[0]])

cluster1, cluster2, cluster3 = split_clusters(reduced_array, cluster_labels)
vote_cluster1, vote_cluster2, vote_cluster3 = split_clusters(transformed_ballots, cluster_labels)

#outputs.plot_pca_ballots(np.array(cluster1), np.array(cluster2), np.array(cluster3), rotated_slates)

#votes1, votes2, votes3 = get_clustered_vote_counts(np.array(vote_cluster1), np.array(vote_cluster2), np.array(vote_cluster3), num_candidates, num_candidates)
#print(votes1)
#outputs.plot_vote_counts(votes1, votes2, votes3, candidates)

#outputs.print_slates(candidates, momentum_slate, left_unity_slate)

#outputs.print_pca_components(pca)

# for ballot in transformed_ballots:
#     print(ballot[16])
    #if len(ballot) > 5 and ballot[16] == 16:
        #print(ballot)
# counts, win_order = run_stv(ballots, cluster_labels, num_votes, num_candidates)
# x = 0
# for i in range(num_candidates):
#     if win_order[i] == 1:
#         x += 1
#     print(candidates[i] + ': ' + str('Round ' + str(win_order[i])))
# print(x)