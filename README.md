# deep-gpt-wrapper

## We build a cool ML tool
Oxxo is one of the most popular convenience stores in Mexico, they've recently faced a problem to determine weather a location (lat, lon) will be a successfull location for their store. Our goal is to develop a predictive model that can assess this issue by receiving the latitude and longitude as input

## How does it work?
We will leverage Computer vision and classification machine learning to scan the several customers that enter a user's store, classifying customers into safe, suspicious, and dangerous based on their movements inside the store. Once they are detected to be dangerous, three things happen. We will send a Whatsapp notification to the shop owner, notifyig them of the unusual behvaior in their store.  We will also run object recognition and facial recognition to determine what was stolen and who did. After all of these are finished, we display to the user a report providing further details about the situation. We also have several other features as part of our intricate dashboard, including a heatmap of the "hot zones" where shoplifting is most common. 

## Our features
- ✅ View heatmap of Oxxo stores in the Monterrey metropolitan area
- ✅ Map division in importance zones for the company
- ✅ Return Top 3 stores depending on a selected location
- ✅ Provide additional insights from internal data for each store selected
- ✅ Use of GradientBoostingRegressor model with r-squared = .83
- ✅ Used external data-sets for schools, 911 reports, population-density and close-competition

## Demo 



## Installation

To install all of the dependencies, you'll need to first make a virtual environment like so :
```bash
py -m venv .venv
```
Next, you'll want to activate the venv like so:
```bash
.venv/Scripts/activate
```
Now navigate to the `backend` directory.
Then, you'll want to install all backend dependencies:
```bash
pip install -r requirements.txt
```

Also, please note that this is a project built on top of Streamlit, and so you'll need a `.streamlit` folder with a `secrets.toml` file with all of your streamlit api keys.


## Contributors

<a href="https://github.com/JocelynVelarde/Hack-Harvard-2024/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JocelynVelarde/Hack-Harvard-2024" />
</a>
