import cdsapi
import argparse
import os
from subprocess import call

all_years = [
    '1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993',
    '1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008',
    '2009','2010','2011','2012','2013','2014','2015','2016','2017','2018'
]
all_months = [
    '01','02','03','04','05','06','07','08','09','10','11','12'
]
all_days = [
    '01','02','03','04','05','06','07','08','09','10','11','12','13','14','15',
    '16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'
]
# all_times = [
#     '00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00',
#     '09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00',
#     '18:00','19:00','20:00','21:00','22:00','23:00'
# ]
all_times = [
    '00:00', '06:00', '12:00','18:00',
]
pressure_level =['50', '100', '150', '200', '250', '300', '400', '500', '600', '700', '850', '925', '1000']

upper_air_variables = [
            'geopotential', 'specific_humidity', 'temperature',
            'u_component_of_wind', 'v_component_of_wind',
         ],
surface_variables =[
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
            'mean_sea_level_pressure',
       ]
constant_variables =['land_sea_mask','orography', 'soil_type']

def idmDownloader(task_url, folder_path, file_name):
    """
    IDM下载器
    :param task_url: 下载任务地址
    :param folder_path: 存放文件夹
    :param file_name: 文件名
    :return:
    """
    # IDM安装目录
    idm_engine = "S:\\IDM.6.38\\Internet Download Manager\\IDMan.exe"
    # 将任务添加至队列
    call([idm_engine, '/d', task_url, '/p', folder_path, '/f', file_name, '/a'])
    # 开始任务队列
    call([idm_engine, '/s'])
def download_single_file(
        variable,
        level_type,
        output_dir,
        year,
        pressure_level=[],
        month=all_months,
        day=all_days,
        time=all_times,
        custom_fn=None
):
    """
    Download a single file from the ERA5 archive.

    :param variable: Name of variable in archive
    :param level_type: 'single' or 'pressure'
    :param output_dir: Directory where file is stored
    :param year: Year(s) to download data
    :param pressure_level: Pressure levels to download. None for 'single' output type.
    :param month: Month(s) to download data
    :param day: Day(s) to download data
    :param time: Hour(s) to download data. Format: 'hh:mm'
    :param custom_fn: If not None, use custom file name. Otherwise infer from parameters.
    """

    fn = custom_fn or (
        '_'.join(variable + pressure_level + year) + '_raw.nc'
    )

    c = cdsapi.Client()

    request_parameters = {
        'product_type':   'reanalysis',
        'format':         'netcdf',
        'variable':       variable,
        'year':           year,
        'month':          month,
        'day':            day,
        'time':           time,
    }
    request_parameters.update({'pressure_level': pressure_level} if level_type == 'pressure' else {})

    r = c.retrieve(
        f'reanalysis-era5-{level_type}-levels',
        request_parameters,
    )
    url = r.location  # 获取文件下载地址
    # path = os.path.join(output_dir ,   fn) # 存放文件夹
    idmDownloader(url, output_dir, fn)  # 添加进IDM中下载
 
if __name__ == '__main__':
    
    level_type = 'single'
    
    output_dir = f'D:\DGGS\letter2\WeatherBench\ERA5'
    
    year = ['2018']
    
    pressure_level = []
    
    variable= surface_variables[2]
    
    custom_fn = f'{variable}_{year[0]}_{all_months[0]}.nc'
    
    download_single_file(
        variable,
        level_type,
        output_dir,
        year,
        pressure_level=[],
        month=all_months[0],
        day=all_days,
        time=all_times,
        custom_fn=custom_fn
        )
