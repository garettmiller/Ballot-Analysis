import matplotlib.pyplot as plt


def write_candidate_and_value(f, candidates, values):
    for i in range(len(candidates)):
        f.write(candidates[i] + ': ' + str(values[i]) + '\n')


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

        plt.savefig('output_files/2021/pca_components/component' + str(i + 1) + '.png')


def plot_pca_ballots(cluster1, cluster2, cluster3, cluster4, cluster5, cluster6, rotated_slates, cluster_names):
    legend_labels = list(cluster_names.keys())
    legend_labels.append("Slate Voting Guides")

    group1, = plt.plot(cluster1[:, 0], cluster1[:, 1], 'ro')
    group2, = plt.plot(cluster2[:, 0], cluster2[:, 1], 'yo')
    group3, = plt.plot(cluster3[:, 0], cluster3[:, 1], 'bo')
    group4, = plt.plot(cluster4[:, 0], cluster4[:, 1], 'mo')
    group5, = plt.plot(cluster5[:, 0], cluster5[:, 1], 'co')
    group6, = plt.plot(cluster6[:, 0], cluster6[:, 1], 'go')
    group7, = plt.plot(rotated_slates[:, 0], rotated_slates[:, 1], 'k*')
    plt.legend([group1, group2, group3, group4, group5, group6, group7], legend_labels)
    plt.title("Voter Plot Principal Axes 1 and 2")
    plt.xlabel("Principal Axis 1: Caucus")
    plt.ylabel("Principal Axis 2: Buxmont")
    plt.savefig('output_files/2021/vote_plots/PCA12.png')
    plt.clf()

    # group1, = plt.plot(cluster1[:, :1], cluster1[:, 2:3], 'yo')
    # group2, = plt.plot(cluster2[:, :1], cluster2[:, 2:3], 'ro')
    # group3, = plt.plot(cluster3[:, :1], cluster3[:, 2:3], 'bo')
    # group4, = plt.plot(rotated_slates[:, :1], rotated_slates[:, 2:3], 'g*', label="Slate Voting Guides")
    # plt.legend((group1, group2, group3, group4), ("Unaligned", "Bread and Roses", "Left Unity", "Slate Voting Guides"))
    # plt.title("Voter Plot Principal Axes 1 and 3")
    # plt.xlabel("Principal Axis 1: Caucus")
    # plt.ylabel("Principal Axis 3: Uncast Votes")
    # #plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    # plt.savefig('output_files/2021/vote_plots/PCA13.png')
    # plt.clf()
    #
    # group1, = plt.plot(cluster1[:, :1], cluster1[:, 5:6], 'yo')
    # group2, = plt.plot(cluster2[:, :1], cluster2[:, 5:6], 'ro')
    # group3, = plt.plot(cluster3[:, :1], cluster3[:, 5:6], 'bo')
    # group4, = plt.plot(rotated_slates[:, :1], rotated_slates[:, 5:6], 'g*', label="Slate Voting Guides")
    # plt.legend((group1, group2, group3, group4), ("Unaligned", "Bread and Roses", "Left Unity", "Slate Voting Guides"))
    # plt.title("Voter Plot Principal Axes 1 and 6")
    # plt.xlabel("Principal Axis 1: Caucus")
    # plt.ylabel("Principal Axis 6: Identity")
    # #plt.legend(["Unaligned", "Left Unity", "Momentum", "Slate Voting Guides"])
    # plt.savefig('output_files/2021/vote_plots/PCA16.png')
    # plt.clf()


def print_slates(candidates, momentum_slate, left_unity_slate):
    print("Bread and Roses Slate")
    for x in momentum_slate[0]:
        print(candidates[x - 1])

    print("\nLeft Unity Slate")
    for x in left_unity_slate[0]:
        print(candidates[x - 1])


def plot_vote_counts(clusters, candidates, cluster_names):
    for candidate_index in range(len(candidates)):
        clustered_vote_counts = [cluster[candidate_index, 1:45] for cluster in clusters]

        clustered_bars = []
        f = open('output_files/2021/vote_counts/numbers/' + candidates[candidate_index] + '.txt', 'w')
        bottom = [0] * 44
        for i in range(len(clustered_vote_counts)):
            f.write(list(cluster_names.keys())[i] + ': ' + str(clustered_vote_counts[i]) + '\n')

            bar = plt.bar(range(1, 45), clustered_vote_counts[i], bottom=bottom, color=list(cluster_names.values())[i])
            bottom = bottom + clustered_vote_counts[i]
            clustered_bars.append(bar)

        f.close()
        if candidates[candidate_index] == "Anlin Wang":
            print("hello")
        plt.legend(clustered_bars, list(cluster_names.keys()))
        plt.title("Vote Distribution for " + candidates[candidate_index])
        plt.xlabel("Score Assigned")
        plt.ylabel("Number of Votes")
        plt.ylim((0, 130))
        plt.savefig('output_files/2021/vote_counts/images/' + candidates[candidate_index] + ".png")
        plt.clf()


def print_pca_components(pca):
    for i in range(len(pca.components_)):
        f = open('output_files/2021/pca_components/textfiles/component' + str(i+1) + '.txt', "w")
        f.write(str(pca.components_[i]))
        f.close()


def print_totals(pca, cluster_counts, cluster_names):
    f = open('output_files/2021/totals.txt', 'w')
    # print(pca.noise_variance_)
    # print(pca.explained_variance_)

    #cluster_titles = ['Momentum', 'Left Unity', 'Unaligned']

    f.write('Ballot Analysis Totals')

    f.write('\n\nCluster Counts\n')
    for cluster in range(len(cluster_counts)):
        f.write('Voters in ' + list(cluster_names.keys())[cluster] + ': ' + str(cluster_counts[cluster]) + '\n')

    f.write('\n\n\nExplained Variance Ratios by Component\n')
    for component in range(len(pca.explained_variance_ratio_)):
        f.write('Component ' + str(component + 1) + ': ' + str(pca.explained_variance_ratio_[component]) + '\n')
    f.close()


def write_cluster_centers(cluster_centers, candidates, cluster_names):
    for i in range(len(cluster_centers)):
        f = open('output_files/2021/clusters/cluster' + str(i + 1) + '.txt', "w")
        f.write(list(cluster_names.keys())[i] + ' Cluster Location\n\n')
        write_candidate_and_value(f, candidates, cluster_centers[i])
        f.close()


def write_diff_cluster_centers(cluster_centers, candidates, cluster_names, compared_clusters):
    f = open('output_files/2021/clusters/diffs/clusterdiff' + str(compared_clusters[0] + 1) + str(compared_clusters[1] + 1) + '.txt', "w")
    cluster_name_keys = list(cluster_names.keys())
    f.write(cluster_name_keys[compared_clusters[0]] + ' minus '+ cluster_name_keys[compared_clusters[1]] + ' Cluster Diff\n\n')
    write_candidate_and_value(f, candidates, cluster_centers[compared_clusters[0]] - cluster_centers[compared_clusters[1]])
    f.close()

