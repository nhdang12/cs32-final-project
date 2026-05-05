Our final project is a recipe scraper that receives user specifications such as available ingredients, unwanted ingredients, and available time as inputs and outputs a ranked list of recipes from a loaded database based on how well they satisfy the inputs. Additional functionality includes being able to save favorite recipes which influences the scoring algorithm of recipes to favor recipes that share ingredients with saved recipes. 

The code can be run directly from the terminal by running main.py. 

Our recipe database (recipes.csv) came from a Kaggle dataset (https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life/data). Our code also allows for user-inputted recipe databases that are in the same .csv format. 

Generative AI was used to help with the file loading (cleaning inputs, implementing reg ex, filtering common extraneous words in recipes) and the scoring system (tweaking the equation to account for proportion of matched ingredients and optimizing weights).
