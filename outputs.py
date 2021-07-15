import matplotlib.pyplot as plt


def write_candidate_and_value(f, candidates, values):
    for i in range(len(candidates)):
        f.write(candidates[i] + ": " + str(values[i]) + "\n")


def plot_important_pca_components(pca, candidates, threshold, output_location):
    """Plot the most important axes of the import PCA components"""
    for i in range(6):
        component = pca.components_[i]
        important_candidates = []
        important_values = []
        for j in range(len(component)):
            if component[j] > threshold or component[j] < -threshold:
                important_candidates.append(candidates[j])
                important_values.append(component[j])

        plt.figure(figsize=(10, 10))
        plt.bar(important_candidates, important_values)
        plt.xticks(rotation=30)
        plt.title("PCA Component " + str(i + 1) + " Most Important Candidates")
        plt.xlabel("Candidate")
        plt.ylabel("Candidate's Relative Alignment to Component")

        plt.savefig(output_location + "pca_components/graphs/component" + str(i + 1) + ".png")


def plot_ballots_pca(clusters, pca_slates, cluster_names, x_pca_index, y_pca_index, x_pca_description, y_pca_description, output_location):
    """Create 2 dimensional plots using the selected PCA components. Clusters are color-coded"""
    legend_labels = list(cluster_names.keys())
    x_index_label = str(x_pca_index + 1)
    y_index_label = str(y_pca_index + 1)
    groups = []

    for i in range(len(clusters)):
        color = list(cluster_names.values())[i]
        group, = plt.plot(clusters[i][:, 0], clusters[i][:, 2], color + "o")
        groups.append(group)

    legend_labels.append("Slate Voting Guides")
    slates, = plt.plot(pca_slates[:, 0], pca_slates[:, 2], "k*")
    groups.append(slates)

    plt.legend(groups, legend_labels)
    plt.title("Voter Plot Principal Axes " + x_index_label + " and " + y_index_label)
    plt.xlabel("Principal Axis " + x_index_label + ": " + x_pca_description)
    plt.ylabel("Principal Axis " + y_index_label + ": " + y_pca_description)
    plt.savefig(output_location + "vote_plots/PCA" + x_index_label + y_index_label + ".png")
    plt.clf()


def plot_candidate_vote_distributions(clusters, candidates, cluster_names, output_location):
    """Plot graph and write text file of each candidate with a cluster coded distribution of votes (vectorized)"""
    for candidate_index in range(len(candidates)):
        clustered_vote_counts = [cluster[candidate_index, 1:45] for cluster in clusters]

        clustered_bars = []
        f = open(output_location + "vote_counts/numbers/" + candidates[candidate_index] + ".txt", "w")
        bottom = [0] * 44
        for i in range(len(clustered_vote_counts)):
            f.write(list(cluster_names.keys())[i] + ": " + str(clustered_vote_counts[i]) + "\n")

            bar = plt.bar(range(1, 45), clustered_vote_counts[i], bottom=bottom, color=list(cluster_names.values())[i])
            bottom = bottom + clustered_vote_counts[i]
            clustered_bars.append(bar)

        f.close()

        plt.legend(clustered_bars, list(cluster_names.keys()))
        plt.title("Vote Distribution for " + candidates[candidate_index])
        plt.xlabel("Score Assigned")
        plt.ylabel("Number of Votes")
        plt.ylim((0, 130))
        plt.savefig(output_location + "vote_counts/images/" + candidates[candidate_index] + ".png")
        plt.clf()


def write_pca_components_by_candidate(pca, candidates, output_location):
    """Write text files with new PCA axes and each components representation on that axis"""
    for i in range(len(pca.components_)):
        f = open(output_location + "pca_components/textfiles/component" + str(i+1) + ".txt", "w")
        f.write("PCA Component " + str(i + 1) + "\n\n")
        write_candidate_and_value(f, candidates, pca.components_[i])
        f.close()


def write_cluster_counts(cluster_counts, cluster_names, output_location):
    """Write text file with names of clusters and number of members."""
    f = open(output_location + "cluster_counts.txt", "w")

    f.write("Ballot Analysis Totals")
    f.write("\n\nCluster Counts\n")
    for cluster in range(len(cluster_counts)):
        f.write("Voters in " + list(cluster_names.keys())[cluster] + ": " + str(cluster_counts[cluster]) + "\n")


def write_pca_variances(pca, output_location):
    """Write text file with PCA components and percent variance explained for each"""
    f = open(output_location + "pca_variances.txt", "w")

    f.write("\n\n\nExplained Variance Ratios by Component\n")
    for component in range(len(pca.explained_variance_ratio_)):
        f.write("Component " + str(component + 1) + ": " + str(pca.explained_variance_ratio_[component]) + "\n")
    f.close()


def write_cluster_centers(cluster_centers, candidates, cluster_names, output_location):
    for i in range(len(cluster_centers)):
        f = open(output_location + "clusters/cluster" + str(i + 1) + ".txt", "w")
        f.write(list(cluster_names.keys())[i] + " Cluster Location\n\n")
        write_candidate_and_value(f, candidates, cluster_centers[i])
        f.close()


def write_diff_cluster_centers(cluster_centers, candidates, cluster_names, compared_clusters, output_location):
    f = open(output_location + "clusters/diffs/clusterdiff" + str(compared_clusters[0] + 1) + str(compared_clusters[1] + 1) + ".txt", "w")
    cluster_name_keys = list(cluster_names.keys())
    f.write(cluster_name_keys[compared_clusters[0]] + " minus "+ cluster_name_keys[compared_clusters[1]] + " Cluster Diff\n\n")
    write_candidate_and_value(f, candidates, cluster_centers[compared_clusters[0]] - cluster_centers[compared_clusters[1]])
    f.close()


def get_ballot_string(ballot, candidates):
    return str([candidates[i - 1] for i in ballot])


def ballot_query(query_dictionary, ballots, cluster_labels, cluster_names, candidates, output_location):
    file_name = output_location + "queries/"
    description_string = ""
    candidate_names = list(candidates.values())
    selected_voter_indices = []

    for name in list(query_dictionary.keys()):
        candidate_index = 0

        for i in range(len(candidate_names)):
            if name == candidate_names[i]:
                candidate_index = i + 1
                break
        
        for i in range(len(ballots)):
            if len(ballots[i]) > query_dictionary[name] and  ballots[i][query_dictionary[name]] == candidate_index:
                selected_voter_indices.append(i)

        file_name = file_name + name + str(query_dictionary[name])
        description_string = name + " at position " + str(query_dictionary[name]) + " and "

    file_name = file_name + ".txt"
    f = open(file_name, "w")

    f.write("This file contains all voters who voted for " + description_string + "\n\n")
    for i in selected_voter_indices:
        f.write("Voter " + str(i) + " in " + list(cluster_names.keys())[cluster_labels[i]] + ": " + get_ballot_string(ballots[i], candidates) + "\n")


def plot_cluster_number_variances(cluster_choices, cluster_variances, output_location):
    plt.plot(cluster_choices, cluster_variances, "bx-")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Variance Explained")
    plt.title("The Elbow Method showing the optimal k")
    plt.savefig(output_location + "node_numbers.png")

