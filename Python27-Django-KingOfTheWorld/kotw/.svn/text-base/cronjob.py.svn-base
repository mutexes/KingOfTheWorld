#full path too djangoproject root
djangoproject_root = "/home/Ellis/CMPT470-1131-g-team-lazy/kotw/"

import sys,os
sys.path.append(djangoproject_root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from countries.models import Country, Build, Army, Tech, Resource
from techs.models import Tech as Techs
from buildings.models import Building
from governments.models import Government, effects

econ_tech=Techs.objects.get(type="Economics").effect_val
res_tech=Techs.objects.get(type="Residential").effect_val
geo_tech=Techs.objects.get(type="Geography").effect_val

enterprise_mod=Building.objects.get(type="enterprise").effect_val
industrial_mod=Building.objects.get(type="industrial").effect_val
farm_mod=Building.objects.get(type="farm").effect_val
oil_mod=Building.objects.get(type="oil_rig").effect_val
unused_mod=Building.objects.get(type="unused").effect_val

gov_income_con=effects.objects.get(effect_name="decrease income").effect_val
gov_income_pro=effects.objects.get(effect_name="increase income").effect_val

gov_prod_con=effects.objects.get(effect_name="decrease resource production").effect_val
gov_prod_pro=effects.objects.get(effect_name="increase resource production").effect_val

gov_tech_con=effects.objects.get(effect_name="decrease technology effectiveness").effect_val
gov_tech_pro=effects.objects.get(effect_name="increase technology effectiveness").effect_val

gov_pop_con=effects.objects.get(effect_name="decrease population").effect_val



country_list=Country.objects.all()
for c in country_list:
	b=Build.objects.get(country=c)
	a=Army.objects.get(country=c)
	t=Tech.objects.get(country=c)
	r=Resource.objects.get(country=c)
	#update gold
	base_income=r.pop*4.5
	# print "base_income: " + str(base_income)
	if c.government=='C':
		base_income=base_income*gov_income_con
	elif c.government=='R':
		base_income=base_income*gov_income_pro
	econ_mod=1.000+((float(t.economics)/float(r.land))/100)*float(econ_tech)
	# print "econ_mod: " + str(econ_mod)
	build_mod=1.000+(float(b.enterprise)/float(r.land))*float(enterprise_mod)
	# print "build_mod: " + str(build_mod)
	base_income=base_income*build_mod*econ_mod
	# print "mod_income: " + str(base_income)
	military_upkeep=((a.jets*25)+(a.turrets*25)+(a.tanks*50)+(a.troops*12))*(1-b.industry/r.land*industrial_mod)
	# print "mod_upkeep: " + str(military_upkeep)
	net_income=base_income-float(military_upkeep)
	# print "net_income: " + str(net_income)
	r.gold=r.gold+int(net_income)

	#update food
	base_food = (b.farm*farm_mod)+(b.unused*unused_mod)
	# print "base_food: " + str(base_food)
	food_tech_mod=1+((t.geography/r.land)/100*geo_tech)
	# print "food_tech_mod: " + str(food_tech_mod)
	if c.government=='F':
		base_food=base_food*gov_prod_pro
	elif c.government=='DE':
		base_food=base_food*gov_prod_con
		food_tech_mod=food_tech_mod*gov_tech_pro
	elif c.government=='T':
		food_tech_mod=food_tech_mod*gov_tech_con
	base_food=base_food*food_tech_mod
	# print "mod_food: " + str(base_food)
	food_consume = r.pop*0.3+a.troops*0.5
	# print "food_consume: " + str(food_consume)
	net_food = r.food * 0.95 + float(base_food) - food_consume
	# print "net_food: " + str(net_food)
	r.food=int(net_food)

	#update oil
	base_oil = (b.oil*oil_mod)
	# print "base_oil: " + str(base_oil)
	oil_tech_mod=1+((t.geography/r.land)/100*geo_tech)
	# print "oil_tech_mod: " + str(oil_tech_mod)
	if c.government=='F':
		base_oil=base_oil*gov_prod_pro
	elif c.government=='DE':
		base_oil=base_oil*gov_prod_con
		oil_tech_mod=oil_tech_mod*gov_tech_pro
	elif c.government=='T':
		oil_tech_mod=oil_tech_mod*gov_tech_con
	base_oil=base_oil*oil_tech_mod
	# print "net_oil: " + str(base_oil)
	r.oil=r.oil+int(base_oil)

	#update pop
	# print "r.pop: " + str(r.pop)
	built_land=b.enterprise+b.residence+b.industry+b.army+b.labs+b.farm+b.oil
	base_pop = built_land*100+b.unused*50+b.residence*100
	# print "base_max_pop: " + str(base_pop)

	pop_tech_mod=1+((t.residential/r.land)/100*res_tech)
	# print "pop_tech_mod: " + str(pop_tech_mod)
	if c.government=='F':
		base_pop=base_pop*gov_pop_con
	elif c.government=='DE':
		pop_tech_mod=pop_tech_mod*gov_tech_pro
	elif c.government=='T':
		pop_tech_mod=pop_tech_mod*gov_tech_con
	base_pop=base_pop*pop_tech_mod
	max_pop=base_pop
	# print "mod_max_pop: " + str(max_pop)
	current_pop=a.troops+r.pop
	# print "current_pop: " + str(current_pop)
	pop_growth = int(r.pop*0.1)
	# print "pop_growth: " + str(pop_growth)
	if current_pop < max_pop:
		if pop_growth > max_pop-current_pop:
			current_pop=max_pop
		else:
			current_pop=current_pop + pop_growth
	elif current_pop > max_pop:
		current_pop=int(current_pop*0.95)
	if (current_pop-a.troops)<=0:
		r.pop=0
	else:
		r.pop=current_pop-a.troops
		# print "r.pop: " + str(r.pop)
	r.save()

print "CRONJOB OK"