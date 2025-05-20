{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "5f1936f9-08dd-4c09-a973-fd1dc678a268",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 191541 entries, 0 to 191540\n",
      "Data columns (total 3 columns):\n",
      " #   Column                   Non-Null Count   Dtype \n",
      "---  ------                   --------------   ----- \n",
      " 0   Drug_1                   191541 non-null  object\n",
      " 1   Drug_2                   191541 non-null  object\n",
      " 2   Interaction Description  191541 non-null  object\n",
      "dtypes: object(3)\n",
      "memory usage: 4.4+ MB\n",
      "None\n",
      "                Drug_1       Drug_2  \\\n",
      "0           Trioxsalen  Verteporfin   \n",
      "1  Aminolevulinic acid  Verteporfin   \n",
      "2     Titanium dioxide  Verteporfin   \n",
      "3     Tiaprofenic acid  Verteporfin   \n",
      "4          Cyamemazine  Verteporfin   \n",
      "\n",
      "                             Interaction Description  \n",
      "0  Trioxsalen may increase the photosensitizing a...  \n",
      "1  Aminolevulinic acid may increase the photosens...  \n",
      "2  Titanium dioxide may increase the photosensiti...  \n",
      "3  Tiaprofenic acid may increase the photosensiti...  \n",
      "4  Cyamemazine may increase the photosensitizing ...  \n",
      "Index(['Drug_1', 'Drug_2', 'Interaction Description'], dtype='object')\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "# Load the CSV file\n",
    "file_path = \"dataset/Drug_Drug Interactions/db_drug_interactions.csv\"  # Update this if needed\n",
    "df = pd.read_csv(file_path)\n",
    "\n",
    "# Display basic information about the dataset\n",
    "print(df.info())\n",
    "\n",
    "# Display the first few rows to understand the structure\n",
    "print(df.head())\n",
    "print(df.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5ec3f5e1-619c-4394-a99b-2dd620fc25d3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Verteporfin']\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.neighbors import NearestNeighbors\n",
    "\n",
    "\n",
    "# Drop NaN values in Interaction Description\n",
    "df = df.dropna(subset=['Interaction Description'])\n",
    "\n",
    "# TF-IDF Vectorization (with memory optimization)\n",
    "vectorizer = TfidfVectorizer(max_features=5000)  # Limit features to reduce memory usage\n",
    "tfidf_matrix = vectorizer.fit_transform(df['Interaction Description'])\n",
    "\n",
    "# Compute similarity using KNN\n",
    "knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='auto')\n",
    "knn.fit(tfidf_matrix)\n",
    "\n",
    "# Function to recommend similar drugs based on interaction description\n",
    "def recommend_drugs(drug_name, df, knn_model, tfidf_matrix, vectorizer):\n",
    "    # Find interactions involving the given drug\n",
    "    mask = (df['Drug_1'] == drug_name) | (df['Drug_2'] == drug_name)\n",
    "    related_drugs = df[mask][['Drug_1', 'Drug_2']].values.flatten()\n",
    "    related_drugs = set(related_drugs) - {drug_name}  # Remove the searched drug itself\n",
    "\n",
    "    # Get top 5 most similar interaction descriptions\n",
    "    if not related_drugs:\n",
    "        try:\n",
    "            # Transform the drug interaction description into TF-IDF space\n",
    "            drug_desc_vector = vectorizer.transform(df[df['Drug_1'] == drug_name]['Interaction Description'])\n",
    "            distances, indices = knn_model.kneighbors(drug_desc_vector, n_neighbors=5)\n",
    "\n",
    "            # Retrieve drug names from indices\n",
    "            similar_drugs = df.iloc[indices[0]]['Drug_1'].tolist() + df.iloc[indices[0]]['Drug_2'].tolist()\n",
    "            return list(set(similar_drugs) - {drug_name})\n",
    "        except:\n",
    "            return [\"No known interactions found.\"]\n",
    "    \n",
    "    return list(related_drugs)\n",
    "\n",
    "# Example usage\n",
    "drug_name = \"Trioxsalen\"  # Replace with an actual drug from your dataset\n",
    "recommendations = recommend_drugs(drug_name, df, knn, tfidf_matrix, vectorizer)\n",
    "print(recommendations)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "a3d119b5-ecea-4984-8325-1f53eb6c979d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Trioxsalen' 'Aminolevulinic acid' 'Titanium dioxide' 'Tiaprofenic acid'\n",
      " 'Cyamemazine' 'Temoporfin' 'Methoxsalen' 'Hexaminolevulinate'\n",
      " 'Benzophenone' 'Riboflavin' 'Carprofen' 'Cyclophosphamide' 'Paclitaxel'\n",
      " 'Docetaxel' 'Cabazitaxel' 'Sulpiride' 'Rifabutin' 'Phenytoin'\n",
      " 'Rifampicin' 'Fosphenytoin']\n"
     ]
    }
   ],
   "source": [
    "print(df['Drug_1'].unique()[:20])  # Show first 20 unique drug names\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
