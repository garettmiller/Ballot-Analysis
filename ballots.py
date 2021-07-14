import opavote


lu_slate = [["Anlin Wang", "Sal H", "Julia Alekseyeva", "Meag Jae Kaman", "Ron Joseph", "Austin Binns", "Melissa Duvelsdorf",
                     "Aliyah Bixby-Driesen", "Michele Rossi", "Shawn Hogan", "Sanwal Yousaf", "Emily Berkowitz", "Matt Chewning",
                     "Francisco Diez", "Will M", "Matthew Zanowic", "Mike Dewar", "Sam Layding", "Patrick Wargo", "Daisy Confoy", "Rebecca Johnson"]]
br_slate = [["Bill Bradley", "John Campbell", "Amanda Fox", "Dave Fox", "Ethan Hill", "K.T. Liberato"]]
num_clusters = 6
cluster_names = {"LU": "r",
                 "Momentum": "y",
                 "Unaligned (big names)": "b",
                 "LU Plus": "m",
                 "Unaligned (random)": "c",
                 "B&R + SA": "g"}

# Read in ballots, run PCA, and make PCA plots
OpaVote = opavote.OpaVote("include/2021ballots.txt", "output_files/2021/")
OpaVote.write_pca_variances()
OpaVote.plot_important_pca_components()
OpaVote.write_pca_components_by_candidate()

# Transform user defined slates using PCA
slates = [br_slate, lu_slate]
pca_slates = OpaVote.transform_slates(slates)

# Load in clusters and make cluster plots
#OpaVote.plot_cluster_number_variances()
#OpaVote.generate_clusters(num_clusters)
OpaVote.load_clusters()
OpaVote.write_diff_cluster_centers([3, 0])
OpaVote.plot_ballots_pca(pca_slates, 0, 2, "LU vs. Momentum", "B&R + SA")
OpaVote.write_cluster_counts(cluster_names)
OpaVote.plot_candidate_vote_distributions(cluster_names)

# Build query dictionary and search ballots
query = {
    "Katie Bohri": 0
}
opavote.query_ballots(query)


