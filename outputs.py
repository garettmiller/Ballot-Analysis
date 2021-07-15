import matplotlib.pyplot as plt


def write_candidate_and_value(f, candidates, values):
    for i in range(len(candidates)):
        f.write(candidates[i] + ": " + str(values[i]) + "\n")


def plot_important_pca_components(pca, candidates, threshold, file_locations):
    """Plot the most important axes of the import PCA components"""
    for i in range(len(file_locations)):
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

        plt.savefig(file_locations[i])


def write_pca_components_by_candidate(pca, candidates, file_locations):
    """Write text files with new PCA axes and each components representation on that axis"""
    for i in range(len(file_locations)):
        f = open(file_locations, "w")
        f.write("PCA Component " + str(i + 1) + "\n\n")
        write_candidate_and_value(f, candidates, pca.components_[i])
        f.close()


def write_pca_variances(pca, file_location):
    """Write text file with PCA components and percent variance explained for each"""
    f = open(file_location, "w")

    f.write("\n\n\nExplained Variance Ratios by Component\n")
    for component in range(len(pca.explained_variance_ratio_)):
        f.write("Component " + str(component + 1) + ": " + str(pca.explained_variance_ratio_[component]) + "\n")
    f.close()


def plot_cluster_number_variances(cluster_choices, cluster_variances, file_location):
    plt.plot(cluster_choices, cluster_variances, "bx-")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Variance Explained")
    plt.title("The Elbow Method showing the optimal k")
    plt.savefig(file_location)


def write_cluster_counts(cluster_counts, cluster_names, file_location):
    """Write text file with names of clusters and number of members."""
    f = open(file_location, "w")

    f.write("Ballot Analysis Totals")
    f.write("\n\nCluster Counts\n")
    for cluster in range(len(cluster_counts)):
        f.write("Voters in " + list(cluster_names.keys())[cluster] + ": " + str(cluster_counts[cluster]) + "\n")


def write_cluster_centers(cluster_centers, candidates, cluster_names, file_locations):
    for i in range(len(file_locations)):
        f = open(file_locations, "w")
        f.write(list(cluster_names.keys())[i] + " Cluster Location\n\n")
        write_candidate_and_value(f, candidates, cluster_centers[i])
        f.close()


def write_diff_cluster_centers(cluster_centers, candidates, cluster_names, compared_clusters, file_location):
    f = open(file_location, "w")
    cluster_name_keys = list(cluster_names.keys())
    f.write(cluster_name_keys[compared_clusters[0]] + " minus "+ cluster_name_keys[compared_clusters[1]] + " Cluster Diff\n\n")
    write_candidate_and_value(f, candidates, cluster_centers[compared_clusters[0]] - cluster_centers[compared_clusters[1]])
    f.close()


def plot_ballots_pca(clusters, pca_slates, cluster_names, x_pca_index, y_pca_index, x_pca_description, y_pca_description, file_location):
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
    plt.savefig(file_location)
    plt.clf()


def plot_candidate_vote_distributions(clusters, candidates, cluster_names, text_file_locations, graph_file_locations):
    """Plot graph and write text file of each candidate with a cluster coded distribution of votes (vectorized)"""
    for candidate_index in range(len(candidates)):
        clustered_vote_counts = [cluster[candidate_index, 1:45] for cluster in clusters]

        clustered_bars = []
        f = open(text_file_locations[candidate_index], "w")
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
        plt.savefig(graph_file_locations[candidate_index])
        plt.clf()


def get_ballot_string(ballot, candidates):
    return str([candidates[i - 1] for i in ballot])


def write_queried_ballots(description_string, selected_voter_indices, ballots, candidates, cluster_labels, cluster_names, file_location):
    f = open(file_location, "w")

    f.write("This file contains all voters who voted for " + description_string + "\n\n")
    for i in selected_voter_indices:
        f.write("Voter " + str(i) + " in " + list(cluster_names.keys())[cluster_labels[i]] + ": " + get_ballot_string(ballots[i], candidates) + "\n")


