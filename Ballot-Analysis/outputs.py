import numpy as np
import matplotlib.pyplot as plt


def print_important_components(pca, candidates):
    for i in range(6):
        print('Principle Component ' + str(i+1))
        component = pca.components_[i]
        for j in range(len(component)):
            if component[j] > .1 or component[j] < -.1:
                print(candidates[j] + ': ' + str(component[j]))
        print('\n')


def plot_important_components(pca, candidates):
    for i in range(6):
        component = pca.components_[i]
        important_candidates = []
        important_values = []
        for j in range(len(component)):
            if component[j] > .175 or component[j] < -.175:
                important_candidates.append(candidates[j])
                important_values.append(component[j])

        plt.figure(figsize=(10, 10))
        plt.bar(important_candidates, important_values)
        plt.xticks(rotation = 30)
        plt.title("PCA Component " + str(i + 1) + " Most Important Candidates")
        plt.xlabel("Candidate")
        plt.ylabel("Candidate's Relative Alignment to Component")

        plt.savefig('output_files/pca_components/component' + str(i + 1) + '.png')


def prepare_pca_12_params(cluster1, cluster2, cluster3, rotated_momentum, rotated_left_unity):
    return cluster1[:, :1], cluster1[:, 1:2], 'bo', cluster2[:, :1], cluster2[:, 1:2], 'ro', cluster3[:, :1], cluster3[:, 1:2], 'yo', rotated_momentum[:, :1], rotated_momentum[:, 1:2], 'g*', rotated_left_unity[:, :1], rotated_left_unity[:, 1:2], 'g*'


def prepare_pca_13_params(cluster1, cluster2, cluster3, rotated_momentum, rotated_left_unity):
    return cluster1[:, :1], cluster1[:, 2:3], 'bo', cluster2[:, :1], cluster2[:, 2:3], 'ro', cluster3[:, :1], cluster3[:, 2:3], 'yo', rotated_momentum[:, :1], rotated_momentum[:, 1:2], 'g*', rotated_left_unity[:, :1], rotated_left_unity[:, 1:2], 'g*'


def prepare_pca_16_params(cluster1, cluster2, cluster3, rotated_momentum, rotated_left_unity):
    return cluster1[:, :1], cluster1[:, 5:6], 'bo', cluster2[:, :1], cluster2[:, 5:6], 'ro', cluster3[:, :1], cluster3[:, 5:6], 'yo', rotated_momentum[:, :1], rotated_momentum[:, 1:2], 'g*', rotated_left_unity[:, :1], rotated_left_unity[:, 1:2], 'g*'


def plot_pca_ballots(cluster1, cluster2, cluster3, rotated_momentum, rotated_left_unity):
    plt.plot(*prepare_pca_12_params(np.array(cluster1), np.array(cluster2), np.array(cluster3), rotated_momentum,
                                    rotated_left_unity))
    plt.title("Voter Plot Principal Axes 1 and 2")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 2: Buxmont")
    plt.legend(["Unaligned", "Left Unity", "Momentum","Slate Voting Guides"])
    plt.savefig('output_files/vote_plots/PCA12.png')
    plt.clf()

    plt.plot(*prepare_pca_13_params(np.array(cluster1), np.array(cluster2), np.array(cluster3), rotated_momentum,
                                    rotated_left_unity))
    plt.title("Voter Plot Principal Axes 1 and 3")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 3: Uncast Votes")
    plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    plt.savefig('output_files/vote_plots/PCA13.png')
    plt.clf()

    plt.plot(*prepare_pca_16_params(np.array(cluster1), np.array(cluster2), np.array(cluster3), rotated_momentum,
                                    rotated_left_unity))
    plt.title("Voter Plot Principal Axes 1 and 6")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 6: Identity")
    plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    plt.savefig('output_files/vote_plots/PCA16.png')
    plt.clf()


def print_slates(candidates, momentum_slate, left_unity_slate):
    print("Momentum Slate")
    for x in momentum_slate[0]:
        print(candidates[x - 1])

    print("\nLeft Unity Slate")
    for x in left_unity_slate[0]:
        print(candidates[x - 1])


def plot_vote_counts(vote_counts, candidates):
    print(vote_counts[10, 1:26])
    for candidate_index in range(len(candidates)):
        candidate_vote_counts = vote_counts[candidate_index, 1:26]
        plt.bar(range(1, 26), candidate_vote_counts)
        plt.title("Vote Distribution for " + candidates[candidate_index])
        plt.xlabel("Score Assigned")
        plt.ylabel("Number of Votes")
        plt.savefig('output_files/vote_counts/' + candidates[candidate_index] + ".png")
        plt.clf()


def print_pca_components(pca):
    for i in range(len(pca.components_)):
        f = open('output_files/pca_components/component' + str(i) + '.txt', "w")
        f.write(str(pca.components_[i]))
        f.close()

