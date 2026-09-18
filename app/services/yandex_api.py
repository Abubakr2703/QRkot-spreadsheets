import io
import re
from datetime import datetime, timedelta
from typing import List

import xlsxwriter

from app.core.config import settings
from app.core.yandex_client import YandexDiskClient
from app.models.charity_project import CharityProject
from app.services.constants import HEADER_BG_COLOR, REPORT_SHEET_NAME


def _safe_filename(name: str) -> str:
    """Убирает из имени файла символы, недопустимые в именах файлов."""
    cleaned = re.sub(r'[^\w\s\-.]', '_', name, flags=re.UNICODE)
    cleaned = cleaned.replace(' ', '_')
    return cleaned


def format_time_delta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    if days > 0:
        return (f"{days} дн. {hours} ч.")
    return (f"{hours} ч. {minutes} мин.")


async def create_simple_report(
    projects: List[CharityProject],
    yandex_client: YandexDiskClient,
) -> str:
    now_date_time = datetime.now().strftime(settings.report_format)
    safe_date = _safe_filename(now_date_time)
    filename = f'Отчёт_{safe_date}'
    upload_url, file_path = await yandex_client.create_excel_file(filename)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet(REPORT_SHEET_NAME)

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'border': 1,
    })
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': HEADER_BG_COLOR,
        'font_color': 'white',
        'border': 1,
        'align': 'center',
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'left'})
    total_format = workbook.add_format({
        'bold': True,
        'border': 1,
        'bg_color': '#D9E1F2',
        'align': 'left',
    })

    worksheet.merge_range(
        0, 0, 0, 2, f'Отчёт от {now_date_time}', title_format
    )

    headers = ['Название проекта', 'Время сбора', 'Описание']
    for col, header in enumerate(headers):
        worksheet.write(1, col, header, header_format)

    row = 2
    for project in projects:
        collection_time = format_time_delta(
            project.close_date - project.create_date
        )
        worksheet.write(row, 0, project.name, cell_format)
        worksheet.write(row, 1, collection_time, cell_format)
        worksheet.write(row, 2, project.description, cell_format)
        row += 1

    worksheet.merge_range(
        row, 0, row, 2,
        f'Всего проектов: {len(projects)}',
        total_format,
    )

    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 18)
    worksheet.set_column('C:C', 40)

    workbook.close()
    output.seek(0)

    await yandex_client.upload_file(upload_url, output.getvalue())

    return await yandex_client.publish_file(file_path)
