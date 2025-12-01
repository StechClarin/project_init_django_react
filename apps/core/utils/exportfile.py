import csv
import openpyxl
from django.http import HttpResponse
from datetime import datetime

class ExportFile:
    """
    Utilitaire générique pour transformer une liste de dicts en fichier.
    """

    @staticmethod
    def _get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def to_csv(data: list, filename: str = "export") -> HttpResponse:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{ExportFile._get_timestamp()}.csv"'

        if not data:
            return response

        writer = csv.writer(response)
        # Les clés du premier élément servent d'en-têtes
        headers = list(data[0].keys())
        writer.writerow(headers)

        for item in data:
            # On écrit les valeurs dans l'ordre des en-têtes
            writer.writerow([str(item.get(h, '')) for h in headers])

        return response

    @staticmethod
    def to_excel(data: list, filename: str = "export") -> HttpResponse:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}_{ExportFile._get_timestamp()}.xlsx"'

        if not data:
            return response

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Export"

        headers = list(data[0].keys())
        ws.append(headers)

        for item in data:
            row = []
            for h in headers:
                val = item.get(h, '')
                # Nettoyage des Timezones pour Excel
                if isinstance(val, datetime):
                    val = val.replace(tzinfo=None)
                row.append(val)
            ws.append(row)

        wb.save(response)
        return response