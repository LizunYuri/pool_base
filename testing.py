pool_data = {
        'length' : 6,
        'width' : 3,
        'depth' : 1.5,
        'podium' : 0.3
    }

construction_data = {
        'wall_thickness' : 250, # толщина стен
        'slab_thickness' : 200, # толщина плиты
        'bedding_thickness' : 200, # подсыпка
        'footing_materials' : 0 # подбетонка
    }


# перевод данных в миллиметры

wall_thickness = float(construction_data['wall_thickness'] / 1000) 
slab_thickness = float(construction_data['slab_thickness'] / 1000)

bedding_thickness = float(construction_data['bedding_thickness'] / 1000)
footing_materials = float(construction_data['footing_materials'] / 1000)


length = float(pool_data['length'])
width = float(pool_data['width'])
depth = float(pool_data['depth'])
podium = float(pool_data['podium'])



# получение финального размера стен и площади основания
final_lenght = length + (wall_thickness * 2 )
final_width = width  + (wall_thickness * 2 )
final_volume = (final_lenght * final_width)

# глубина котлована относительно условного 0

final_depth = round((depth + slab_thickness + bedding_thickness + footing_materials) - podium, 2)
pit_volume = final_volume * final_depth # объем котлована
soil_volume = round(pit_volume * 1.5)  # объем грунта

print('площадь', final_volume, 'объем котлована', pit_volume, 'объем груна', soil_volume)


# расчет бетонной плиты

plate_data = {
    'cell' : 200,
    'row' : 2
    }

wall_data = {
        'cell' : 200,
        'row' : 2
    }

volume_concrete = round(final_volume * slab_thickness, 1)

plate_cell = float(plate_data['cell'] / 1000)
plate_row = int(plate_data['row'])

wall_cell = float(wall_data['cell'] / 1000)
wall_row = int(wall_data['row'])


if plate_cell != 0:
    length_reinforcement = round((2 + (final_lenght / plate_cell) * plate_row), 0)
    width_reinforcement = round((2 + (final_width / plate_cell) * plate_row), 0)
    total_cell_plate = (length_reinforcement * final_lenght) + (width_reinforcement * final_width)
    number_of_rods = round((total_cell_plate / 11.8), 0)
else:
    length_reinforcement = 0
    width_reinforcement = 0
    total_cell_plate = 0
    number_of_rods = 0

# расчет бетона и арматуры для стен бассейна

if wall_cell != 0:
    long_wall_concrete = round((final_lenght * depth * wall_cell) * 2, 2)
    long_wall_reinforcement_lenght = round((2 + (final_lenght / wall_cell) * wall_row), 0)
    long_wall_reinforcement_depth = round((2 + (depth / wall_cell) * wall_cell), 0)
    total_long_wall_reinforcement = (long_wall_reinforcement_depth + long_wall_reinforcement_lenght) * 2
    short_wall_concrete = round((final_width * depth * wall_cell) * 2, 2)

    short_wall_reinforcement_width = round((2 + (final_width / wall_cell) * wall_row), 0)
    short_wall_reinforcement_depth = round((2 + (depth / wall_cell) * wall_cell), 0)
    total_short_wall_reinforcement = (short_wall_reinforcement_width + short_wall_reinforcement_depth) * 2

    total_wall_concrete = long_wall_concrete + short_wall_concrete
    total_wall_reinforcement = total_long_wall_reinforcement + total_short_wall_reinforcement

#  reinforcement


print('бетонная плита: количество рядов:', length_reinforcement + width_reinforcement, 'объем бетона:', volume_concrete, 'метров арматуры:', total_cell_plate, 'количество прутов по 11.8м', number_of_rods)
print(
        'Бетон для длинной тенки:', long_wall_concrete, 
        'Бетон для короткой стенки:', short_wall_concrete,  
        'Бетон для стен сумма:', total_wall_concrete, 
        'метров арматуры для длинной стенки:', total_long_wall_reinforcement, 
        'метров арматуры для короткой стенки:', total_short_wall_reinforcement,
        'Итого арматуры для стен', total_wall_reinforcement,
        'Итого арматуры для чаши бассейна: '
        )




# wall_thickness = excavation_data.wall_thickness / 1000

#             slab_thickness = excavation_data.slab_thickness / 1000

#             if excavation_data.bedding_thickness != 0:
#                 bedding_thickness = excavation_data.bedding_thickness / 1000
#             else: 
#                 bedding_thickness = 0
            
#             if excavation_data.footing_materials != 0:
#                 footing_materials = excavation_data.footing_materials / 1000
#             else: 
#                 footing_materials = 0

#             # length = float(size_session_data.get('length', 0))
#             # width = float(size_session_data.get('width', 0))
#             # depth_from = float(size_session_data.get('depth_from', 0))
#             # depth_to = float(size_session_data.get('depth_to', 0))
#             length = float(3)
#             width = float(6)
#             depth_from = float(1.5)
#             depth_to = float(1.5)

#             total_lenght_excavation = (wall_thickness * 2) + length
#             total_width_excavation = (wall_thickness * 2) + width

#             total_plate = (total_lenght_excavation + wall_thickness) + (total_width_excavation + wall_thickness)





#             print('площадь плиты', total_plate, "ширина", width, "длинна", length, "толщина стен", wall_thickness, "общая динна стен", total_lenght_excavation, "общая ширина стен", total_width_excavation)

