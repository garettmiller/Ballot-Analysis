import opavote


lu_slate = [["Anlin Wang", "Sal H", "Julia Alekseyeva", "Meag Jae Kaman", "Ron Joseph", "Austin Binns", "Melissa Duvelsdorf",
                     "Aliyah Bixby-Driesen", "Michele Rossi", "Shawn Hogan", "Sanwal Yousaf", "Emily Berkowitz", "Matt Chewning",
                     "Francisco Diez", "Will M", "Matthew Zanowic", "Mike Dewar", "Sam Layding", "Patrick Wargo", "Daisy Confoy", "Rebecca Johnson"]]
br_slate = [["Bill Bradley", "John Campbell", "Amanda Fox", "Dave Fox", "Ethan Hill", "K.T. Liberato"]]


num_clusters = 8
# cluster_names = {"LU": "r",
#                  "Momentum": "y",
#                  "Unaligned (big names)": "b",
#                  "LU Plus": "m",
#                  "Unaligned (random)": "c",
#                  "B&R + SA": "g"}

# Read in ballots, run PCA, and make PCA plots
OpaVote = opavote.OpaVote("include/2021ballots.txt", "output_files/2021/8_clusters/")
OpaVote.write_pca_variances()
OpaVote.plot_important_pca_components()
OpaVote.write_pca_components_by_candidate()

# Transform user defined slates using PCA
slates = [br_slate, lu_slate]
pca_slates = OpaVote.transform_slates(slates)

# Use this if you don't have names for clusters
cluster_names = OpaVote.generate_cluster_name_dictionary(num_clusters)

# Load in clusters and make cluster plots

OpaVote.generate_clusters(num_clusters)
#OpaVote.load_clusters()
#OpaVote.write_diff_cluster_centers(cluster_names, [1, 5])
OpaVote.plot_cluster_number_variances()
OpaVote.write_cluster_counts(cluster_names)
OpaVote.plot_ballots_pca(pca_slates, cluster_names, 0, 1, "Component 1", "Component 2")
OpaVote.plot_ballots_pca(pca_slates, cluster_names, 0, 2, "Component 1", "Component 3")
OpaVote.plot_ballots_pca(pca_slates, cluster_names, 1, 2, "Component 2", "Component 3")
OpaVote.plot_candidate_vote_distributions(cluster_names)

# Build query dictionary and search ballots
# query = {
#     "Katie Bohri": 0
# }
# opavote.query_ballots(query, cluster_names)


