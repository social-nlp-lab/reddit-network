# read in data from one drive 
# users from the four subreddits
# r/benzodiazepines, r/opiates, r/stims, r/cocaine

library(tidyverse)
library(jsonlite)

dat_path <- "~/OneDrive - Drexel University/Social_NLP_Lab/Datasets/Reddit Drug Data- RAW - DNT/Central/data Dec 1st 2022/data 2018_1_1 to 2022_7_30_"
subs <- c("opiates", "cocaine", "stims", "benzodiazepines")

users <- subs |> map(\(x){
  df <- tibble(read_json(paste0(dat_path, x, "_redditor.json"),
                         simplifyVector = TRUE)[[2]])
}
) |> 
  list_rbind() |> 
  distinct()


posts <- subs |> map(\(x){
  df <- tibble(read_json(paste0(dat_path, x, "_submission.json"),
                         simplifyVector = TRUE)[[2]])
  df <- df |> mutate(subreddit = x)
}
) |> list_rbind()

#########################
# using reddit api to get active users

library(httr)

x <- read_json("https://api.pushshift.io/reddit/search/comment?since=30d&subreddit=science&aggs=author&agg_size=500")
