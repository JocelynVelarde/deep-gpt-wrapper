# deep-gpt-wrapper

![WhatsApp Image 2025-05-25 at 11 52 39](https://github.com/user-attachments/assets/bc10ba99-147e-4cfd-8a8c-bfae8080578a)

## We built a cool ML tool

Oxxo is one of the most popular convenience stores in Mexico, they've recently faced a problem to determine weather a location (lat, lon) will be a successful location for their store. Our goal is to develop a predictive model that can assess this issue by receiving the latitude and longitude as input

- Link to our GitHub repo: https://github.com/JocelynVelarde/deep-gpt-wrapper
- Link to our One-Page dashboard: https://deep-grpt-wrapper.streamlit.app/current-eval

## How does it work?

### Results of Data Cleaning

![WhatsApp Image 2025-05-25 at 11 22 53](https://github.com/user-attachments/assets/7713a6bd-4814-430a-aa78-5e916080b4b3)

### Correlation Matrix

![image](https://github.com/user-attachments/assets/166af7e7-2094-4b56-8fd7-f4781d2f1a1f)

### Sales Distribution by Performance Category

![image](https://github.com/user-attachments/assets/5a82d5cc-f324-443a-a166-e313dc3f63ce)

## Classifying Model

### Confusion Matrix
![WhatsApp Image 2025-05-25 at 13 46 54](https://github.com/user-attachments/assets/88458076-d19b-4d35-8ea4-97020e63b875)

### Feature Importances
![WhatsApp Image 2025-05-25 at 13 47 07](https://github.com/user-attachments/assets/589d4a4c-7092-4f98-b02b-9d9c10d481e3)

### Accuracy: 86.3%

## Regression Model

### Confusion Matrix
![Screenshot from 2025-05-25 14-00-55](https://github.com/user-attachments/assets/035f75b2-88c5-4f01-9728-827c09e548a7)

### Feature Importances
![Screenshot from 2025-05-25 14-01-10](https://github.com/user-attachments/assets/e6d8f2ec-dec0-49ed-a1ff-0a7e3f6ebfa6)

### Accuracy: 45.5%

## Additional store reccommendation

We used gpt-o3-mini model to reccommend between other Oxxo establishments with additional store insights

- Bara
- Caffenio
- Yza Pharmacy

## Our features

- ✅ View heatmap of Oxxo stores in the Monterrey metropolitan area
- ✅ Map division in importance zones for the company
- ✅ Return Top 3 stores depending on a selected location
- ✅ Provide additional insights from internal data for each store selected
- ✅ Use of GradientBoostingClassifier model with r-squared = .83
- ✅ Used external data-sets for schools, 911 reports, population-density and close-competition

## Pitch

https://www.canva.com/design/DAGod445BGw/CcPfUIOo3OAvBohTHOIRzw/edit?utm_content=DAGod445BGw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## External Databases Used

- [911 Reports](https://mide.monterrey.gob.mx/catalogue/uuid/33c3a891-a72d-46c1-af5e-f957e069a585)
- [Schools](https://mide.monterrey.gob.mx/catalogue/uuid/bd4a29cf-3c17-4080-80a6-95cbec757b8a)
- [Location of Oxxo competitors](https://www.inegi.org.mx/app/mapa/denue/default.aspx)
- [Population density per municipality](https://es.wikipedia.org/wiki/Anexo:Municipios_de_Nuevo_Le%C3%B3n)

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

<a href="https://github.com/JocelynVelarde/deep-gpt-wrapper/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JocelynVelarde/deep-gpt-wrapper" />
</a>
