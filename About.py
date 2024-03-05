import streamlit


def main():
    streamlit.header("This is about this project")
    streamlit.subheader("Content based movie recommendation system")

    streamlit.text("""
                This web app is made using streamlit(A Python library)
                
                Skills enhanced: 
                    1. Natural Language processing (a.k.a NLP)
                    2. Machine learning (a.k.a ML)
                    3. Python
                    4. Data fetching and formatting using APIs
                
                The steps used to create movie minds
                Step 1: Data Acquisition
                I acquired 3 datasets of IMDB and TMDB from kaggle, approx 15k Movies from 1996 to 2023
                
                Step 2: Data preprocessing
                Columns used: Title, Genres, Top_3_casts(Actors), directors, writers, 
                Since ML don't understand the textual data, while using NLP, we have to follow certain steps
                
                for the data cleaning and preprocessing
                    1. Remove missing rows and NA values
                    2. Split the textual data to generate usable tokens which will help in analysing the pattern, using NLP
                    3. Having the vector of these split words, create a string
                        - Convert all words into lower case to reduce the repetition like Animal or animal
                        - Apply stemming: Since we focus on the end result and don't have to show the dataset to anybody
                                          We used stemming which converted the words into their root form, to further reduce the 
                                          corpus size.
                        - Make single token for names: For Example: Sam worthington is a director. I tokenized it like Samworthington.
                                                       To analyse it as a single entity
                        - Make a single column 'Tags' which keeps a string of all the textual format prepared to perform model creation
                        steps on it.
                        
                After performing these steps I created a data warehouse where I performed outer join on these three datasets.
                and mapped the movies with their tags.
                The final dataset has 2 columns ['Title', 'Tags'] with approx 13k movies
                
                Step 3: Data visualization
                
                Used python profiler to visualise dataset in form of heatmaps, correlation and confuse matrix.
                
                Step 4: Model creation
                Applied BAG OF WORDS algorithm, with max_features = 13k and removed English stop_words, Used Tags column 
                for this task, which has a mix of all features used to make recommendations
                
                Applied cosine similarity to create the pattern between the movies whether they are similar or not
                can be derived using the similarity matrix of (13k x 13k) movies
                
                and recommends top 5 movies
                
                Step 5: Evaluation
                
                Evaluation is done on the basis of observation. I found some movies as a red flag. 
                I also found many correct recommendations which is the result of training the model on 13k movies.                

    """)
