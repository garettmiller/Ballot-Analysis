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


def plot_pca_ballots(cluster1, cluster2, cluster3, rotated_slates):
    group1, = plt.plot(cluster1[:, :1], cluster1[:, 1:2], 'yo')
    group2, = plt.plot(cluster2[:, :1], cluster2[:, 1:2], 'ro')
    group3, = plt.plot(cluster3[:, :1], cluster3[:, 1:2], 'bo')
    group4, = plt.plot(rotated_slates[:, :1], rotated_slates[:, 1:2], 'g*')
    plt.legend((group1, group2, group3, group4), ("Unaligned", "Momentum", "Left Unity", "Slate Voting Guides"))
    plt.title("Voter Plot Principal Axes 1 and 2")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 2: Buxmont")
    plt.savefig('output_files/vote_plots/PCA12.png')
    plt.clf()

    group1, = plt.plot(cluster1[:, :1], cluster1[:, 2:3], 'yo')
    group2, = plt.plot(cluster2[:, :1], cluster2[:, 2:3], 'ro')
    group3, = plt.plot(cluster3[:, :1], cluster3[:, 2:3], 'bo')
    group4, = plt.plot(rotated_slates[:, :1], rotated_slates[:, 2:3], 'g*', label="Slate Voting Guides")
    plt.legend((group1, group2, group3, group4), ("Unaligned", "Momentum", "Left Unity", "Slate Voting Guides"))
    plt.title("Voter Plot Principal Axes 1 and 3")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 3: Uncast Votes")
    #plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    plt.savefig('output_files/vote_plots/PCA13.png')
    plt.clf()

    group1, = plt.plot(cluster1[:, :1], cluster1[:, 5:6], 'yo')
    group2, = plt.plot(cluster2[:, :1], cluster2[:, 5:6], 'ro')
    group3, = plt.plot(cluster3[:, :1], cluster3[:, 5:6], 'bo')
    group4, = plt.plot(rotated_slates[:, :1], rotated_slates[:, 5:6], 'g*', label="Slate Voting Guides")
    plt.legend((group1, group2, group3, group4), ("Unaligned", "Momentum", "Left Unity", "Slate Voting Guides"))
    plt.title("Voter Plot Principal Axes 1 and 6")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 6: Identity")
    #plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    plt.savefig('output_files/vote_plots/PCA16.png')
    plt.clf()


def print_slates(candidates, momentum_slate, left_unity_slate):
    print("Momentum Slate")
    for x in momentum_slate[0]:
        print(candidates[x - 1])

    print("\nLeft Unity Slate")
    for x in left_unity_slate[0]:
        print(candidates[x - 1])


def plot_vote_counts(cluster1, cluster2, cluster3, candidates):
    for candidate_index in range(len(candidates)):
        candidate_vote_counts1 = cluster1[candidate_index, 1:52]
        candidate_vote_counts2 = cluster2[candidate_index, 1:52]
        candidate_vote_counts3 = cluster3[candidate_index, 1:52]

        f = open('output_files/vote_counts/Numbers/' + candidates[candidate_index] + '.txt', 'w')
        f.write('Momentum: ' + str(candidate_vote_counts1) + '\n')
        f.write('Unaligned: ' + str(candidate_vote_counts2) + '\n')
        f.write('Left Unity ' + str(candidate_vote_counts3) + '\n')
        f.close()

        bar1 = plt.bar(range(1, 52), candidate_vote_counts3, color="r")
        bar2 = plt.bar(range(1, 52), candidate_vote_counts1, color="y")
        bar3 = plt.bar(range(1, 52), candidate_vote_counts2, color="b")

        plt.legend((bar1, bar2, bar3), ("Momentum", "Unaligned", "Left Unity"))
        plt.title("Vote Distribution for " + candidates[candidate_index])
        plt.xlabel("Score Assigned")
        plt.ylabel("Number of Votes")
        plt.ylim((0, 85))
        plt.savefig('output_files/vote_counts/Images/' + candidates[candidate_index] + ".png")
        plt.clf()


def print_pca_components(pca):
    for i in range(len(pca.components_)):
        f = open('output_files/pca_components/textfiles/component' + str(i+1) + '.txt', "w")
        f.write(str(pca.components_[i]))
        f.close()

