import yolo
import calc
import kml

filename = ('34.png')

seeds = yolo.count_seeds(filename)
print(seeds)

sunflowers_count = int(input())
sunflowers_weight = int(input())

sunflower_size = yolo.get_sunflower_size(filename, 15)
print(sunflower_size)
productivity = calc.get_productivity(sunflowers_weight, seeds, sunflowers_count)

coordh = input()
coordw = input()
name = input()
kml.update_file('pole', coordw, coordh, 'дюрбан', productivity, sunflowers_count, sunflowers_weight, name, '1', '1')