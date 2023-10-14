import pygame
import math
pygame.init()

WIDTH, HEIGHT =  1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
GREEN = (34,139,34)
BROWN = (165,42,42)
AU = 149.6e6 * 1000

FONT = pygame.font.SysFont("comicsans", 16)

def format_meters_to_kilometers(meters):
		kilometers = meters / AU
		return f"{kilometers:.3f} AU"

class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 200 / AU  # 1AU = 100 pixels
	TIMESTEP = 1200*24 # 1 day

	def __init__(self, x, y, radius, color, mass, name):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.name = name

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0
		self.perigee = 1000000000000 # large number so first value of perigee will always be smaller
		self.apogee = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2)

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		if not self.sun:
			distance_text = FONT.render(f"{self.name} [{format_meters_to_kilometers(self.perigee)}, {format_meters_to_kilometers(self.apogee)}] ", 1, GREEN)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		self.distance_to_sun = math.sqrt(self.x ** 2 + self.y ** 2) # presuming that sun always stays at center

		if self.distance_to_sun < self.perigee:
			self.perigee = self.distance_to_sun
		elif self.distance_to_sun > self.apogee:
			self.apogee = self.distance_to_sun

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))


def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 'Sun')
	sun.sun = True
	mercury = Planet(0.387 * Planet.AU, 0, 2, DARK_GREY, 3.30 * 10**23, 'Mercury')
	mercury.y_vel = -47.4 * 1000
	venus = Planet(0.723 * Planet.AU, 0, 5.2, WHITE, 4.8685 * 10**24, 'Venus')
	venus.y_vel = -35.02 * 1000


	earth = Planet(-1 * Planet.AU, 0, 6, BLUE, 5.9742 * 10**24, 'Earth')
	earth.y_vel = 29.783 * 1000

	mars = Planet(-1.524 * Planet.AU, 0, 3, RED, 6.39 * 10**23, 'Mars')
	mars.y_vel = 24.077 * 1000

	asteroid = Planet(0.72 * Planet.AU, 0, 3, YELLOW, 4.8685, 'asteroid')
	asteroid.y_vel = -22. * 1000



	planets = [sun, earth, mars, mercury, venus, asteroid]

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()