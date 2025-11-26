import csv
import openpyxl
from io import TextIOWrapper

class ImportFile:
    """
    Utilitaire pour lire des fichiers uploadés et retourner des données structurées.
    """

    @staticmethod
    def parse(uploaded_file) -> list:
        """
        Fonction principale : détecte le type et appelle le bon parseur.
        Retourne une liste de dictionnaires.
        """
        filename = uploaded_file.name
        
        if filename.endswith('.csv'):
            return ImportFile._parse_csv(uploaded_file)
        elif filename.endswith('.xlsx'):
            return ImportFile._parse_excel(uploaded_file)
        else:
            raise ValueError("Format de fichier non supporté. Utilisez .csv ou .xlsx")

    @staticmethod
    def _parse_csv(uploaded_file) -> list:
        """ Lit un CSV et retourne une liste de dicts. """
        file_data = TextIOWrapper(uploaded_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)
        
        data = []
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
            data.append(clean_row)
        return data

    @staticmethod
    def _parse_excel(uploaded_file) -> list:
        """ Lit un Excel et retourne une liste de dicts. """
        wb = openpyxl.load_workbook(uploaded_file)
        ws = wb.active
        
        data = []
        rows = list(ws.iter_rows(values_only=True))
        
        if not rows:
            return []

        headers = [str(h).strip() for h in rows[0] if h] 

        for row in rows[1:]:
            row_dict = dict(zip(headers, row))
            if any(row_dict.values()): 
                data.append(row_dict)
                
        return data