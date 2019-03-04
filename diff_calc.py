import math
def main(file):
	map = file
	objects = []
	radius = (512 / 16) * (1. - 0.7 * (map.cs - 5) / 5);
	class consts:
		decay_base = [0.3,0.15]

		almost_diameter = 90

		aim_angle_bonus_begin = math.pi / 3;
		speed_angle_bonus_begin = 5 * math.pi / 6;
		timing_threshold = 107;

		stream_spacing = 110
		single_spacing = 125

		min_speed_bonus = 75 # 200bpm
		max_speed_bonus = 45 # 330bpm
		speed_balancing_factor = 40

		weight_scaling = [1400,26.25]

		circlesize_buff_threshhold = 30

	class d_obj:
		def __init__(self,base_object, radius,prev):
			self.radius = float(radius)
			self.ho = base_object
			self.strains = [0, 0]
			self.norm_start  = 0
			self.norm_end = 0
			self.prev = prev
			self.delta_time = 0
			# We will scale distances by this factor, so we can assume a uniform CircleSize among beatmaps.
			self.scaling_factor = 52.0 / self.radius
			if self.radius < consts.circlesize_buff_threshhold:
				self.scaling_factor *= 1 + min((consts.circlesize_buff_threshhold - self.radius), 5) / 50.0
			self.norm_start = [float(self.ho.pos[0]) * self.scaling_factor,float(self.ho.pos[1])*self.scaling_factor]
			self.norm_end = self.norm_start
			self.jump_distance = 0
			self.angle = None
			self.travel_distance = 0
			# Calculate jump distance for objects
			if((self.ho.h_type == 1 or self.ho.h_type == 2) and prev != None ):
				self.jump_distance = math.sqrt(math.pow(self.norm_start[0] - prev.norm_end[0],2) + math.pow(self.norm_start[1] - prev.norm_end[1],2))
			# Not working, need to figure out how sliders work
			if(self.ho.h_type == 2):
				self.comp_slider_pos()
			if(prev != None and prev.prev != None):
				# Calculate angle with lastlast last and base object
				v1 = [prev.prev.norm_start[0] - prev.norm_start[0], prev.prev.norm_start[1] - prev.norm_start[1]]
				v2 = [self.norm_start[0] - prev.norm_start[0], self.norm_start[1] - prev.norm_start[1]]
				dot = v1[0]*v2[0] + v1[1]*v2[1]
				det = v1[0]*v2[1] - v1[1]*v2[0]
				self.angle = abs(math.atan2(det,dot))
			if(prev != None):
				self.delta_time = (int(self.ho.time) - int(prev.ho.time)) / map.speed
				if(self.ho.h_type !=  3):
					# Calculate speed
					self.strains[0] = prev.strains[0]*math.pow(consts.decay_base[0],self.delta_time / 1000.0) + self.calculate_speed(prev)*consts.weight_scaling[0]
					# Calculate aim
					self.strains[1] = prev.strains[1]*math.pow(consts.decay_base[1],self.delta_time / 1000.0) + self.calculate_aim(prev)*consts.weight_scaling[1]

		# needs work. Do not understand how sliders work
		def comp_slider_pos(self):
			approx_rad = self.radius * 3
			if self.ho.slider.length > approx_rad:
				self.travel_distance = self.ho.slider.length


		# Calculate aim strain
		def calculate_aim(self,prev):
			result = 0
			strain_time = max(50,self.delta_time)
			prev_strain_time = max(50,prev.delta_time)
			if(prev != None):
				if(self.angle != None and self.angle > consts.aim_angle_bonus_begin):
					scale = 90
					angle_bonus = math.sqrt(max(prev.jump_distance - scale,0) * math.pow(math.sin(self.angle - consts.aim_angle_bonus_begin),2) * max(self.jump_distance - scale,0))
					result = 1.5 * math.pow(max(0,angle_bonus),0.99) / max(consts.timing_threshold, prev_strain_time)
			jump_dist_exp = math.pow(self.jump_distance,0.99)
			travel_dist_exp = 0
			return max(result + jump_dist_exp / max(strain_time, consts.timing_threshold), jump_dist_exp / strain_time)

		# Calculate speed strain
		def calculate_speed(self,prev):
			distance = min(consts.single_spacing, self.jump_distance)
			strain_time = max(50,self.delta_time)
			delta_time = max(consts.max_speed_bonus,self.delta_time)
			speed_bonus = 1.0
			if(delta_time < consts.min_speed_bonus):
				speed_bonus = 1 + math.pow((consts.min_speed_bonus - delta_time) / consts.speed_balancing_factor,2)
			angle_bonus = 1.0
			if(self.angle != None and self.angle < consts.speed_angle_bonus_begin):
				angle_bonus = 1 + math.pow(math.sin(1.5 * (self.angle - consts.speed_angle_bonus_begin)),2) / 3.57
				if(self.angle < math.pi / 2):
					angle_bonus = 1.28
					if(distance < 90 and self.angle < math.pi / 4):
						angle_bonus += (1 - angle_bonus)*min((90 - distance) / 10, 1)
					elif (distance < 90):
						angle_bonus += (1 - angle_bonus)*min((90 - distance) / 10,1) * math.sin(((math.pi / 2 )- self.angle) / (math.pi / 4))
			return (1 + (speed_bonus - 1)*0.75) * angle_bonus * (0.95 + speed_bonus*math.pow(distance / consts.single_spacing,3.5)) / strain_time

	def calculate_difficulty(type, objects):
		strain_step = 400 * map.speed
		prev = None
		max_strain = 0
		decay_weight = 0.9
		highest_strains = []
		interval_end = math.ceil(float(map.objects[0].time) / strain_step) * strain_step
		for obj in objects:
			while int(obj.ho.time) > interval_end:
				highest_strains.append(max_strain)
				if prev == None:
					max_strain = 0
				else:
					decay = math.pow(consts.decay_base[type],(interval_end - int(prev.ho.time)) / 1000.0)
					max_strain = prev.strains[type] * decay
				interval_end += strain_step
			prev = obj
			max_strain = max(obj.strains[type],max_strain)
		highest_strains.append(max_strain)
		difficulty = 0
		weight = 1.0
		highest_strains = sorted(highest_strains, reverse = True)
		for strain in highest_strains:
			difficulty += weight * strain
			weight *= decay_weight
		return difficulty
	star_scaling_factor = 0.0675
	extreme_scaling_factor = 0.5
	prev = None
	for obj in map.objects:
		new = d_obj(obj, radius,prev)
		objects.append(new)
		prev = new
	aim = calculate_difficulty(1, objects)
	speed = calculate_difficulty(0, objects)
	aim = math.sqrt(aim) * star_scaling_factor
	speed = math.sqrt(speed) * star_scaling_factor
	stars = aim + speed + abs(speed-aim) * extreme_scaling_factor
	return [aim,speed,stars, map]