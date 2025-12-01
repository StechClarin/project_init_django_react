import csv
import openpyxl
from io import TextIOWrapper

class ImportFile:
    """
    Utilitaire générique pour lire un fichier et retourner une liste de dicts.
    """

    @staticmethod
    def parse(uploaded_file) -> list:
        filename = uploaded_file.name
        
        if filename.endswith('.csv'):
            return ImportFile._parse_csv(uploaded_file)
        elif filename.endswith('.xlsx'):
            return ImportFile._parse_excel(uploaded_file)
        else:
            raise ValueError("Format de fichier non supporté. Utilisez .csv ou .xlsx")

    @staticmethod
    def _parse_csv(uploaded_file) -> list:
        # TextIOWrapper est nécessaire pour lire le flux binaire en mode texte
        file_data = TextIOWrapper(uploaded_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)
        
        data = []
        for row in reader:
            # Nettoyage des espaces (trim)
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
            data.append(clean_row)
        return data

    @staticmethod
    def _parse_excel(uploaded_file) -> list:
        wb = openpyxl.load_workbook(uploaded_file)
        ws = wb.active
        
        data = []
        rows = list(ws.iter_rows(values_only=True))
        
        if not rows:
            return []

        # La première ligne contient les en-têtes
        headers = [str(h).strip() for h in rows[0] if h] 

        for row in rows[1:]:
            # On associe chaque valeur à son en-tête
            row_dict = dict(zip(headers, row))
            # On ignore les lignes vides
            if any(row_dict.values()): 
                data.append(row_dict)
                
        return data