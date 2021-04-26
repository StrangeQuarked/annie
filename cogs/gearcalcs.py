# import discord
import math
from discord.ext import commands


class Gearcalcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.abilitydict = {
            "bdef": self.calcbdef,
            "bdx": self.calcbdef,
            "bpu": self.calcbpu,
            "iru": self.calcrec,
            "ism": self.calcism,
            "iss": self.calciss,
            "mpu": self.calcmpu,
            "qr": self.calcqr,
            "qsj": self.calcqsj,
            "rec": self.calcrec,
            "res": self.calcinkres,
            "rsu": self.calcrsu,
            "scu": self.calcscu,
            "spu": self.calcspu,
            "ss": self.calcss,
            "ssu": self.calcssu,
        }

    def calcAP(self, string):  # assuming string is entered in 0m0s format
        try:
            stri = string.split("m")
            mains = int(stri[0])
            subs = int(stri[1][0])
        except:
            return "Error: Invalid AP amount entered. AP must be in 0m0s format."
        return 10 * mains + 3 * subs

    def calcPctChange(
        self, basevalue, newvalue
    ):  # to use: input the starting value without any ability chunks, then the value with ability chunks
        return -100 * (1 - (newvalue / basevalue))

    def InterpolationFunction(
        self, b, c
    ):  # b and c are p/100 and s as calculated in the calcAbilityEffects function
        if c == 0.5:
            return b
        elif b == 0.0:
            return b
        elif b == 1.0:
            return b
        elif c != 0.5:
            return 2.71828182846 ** (
                -(math.log(b) * math.log(c)) / math.log(2)
            )  # log is the same as what is normally ln (natural logarithm or log base e) here

    def calcAbilityEffects(
        self, AP, minimum, maximum, mid=0
    ):  # inputs are the number of AP and the minimum possible value of that ability (i.e the value at 0m0s) and the maximum possible value of the ability (the value at 3m9s). Use a gear calculator to get those and input them as the min and max.
        if (
            mid == 0
        ):  # added mid value input since special saver has a mid value that is not the mean of the minimum and maximum values
            mid = (minimum + maximum) / 2
        p = min(
            3.3 * AP - 0.027 * AP ** 2, 100
        )  # p and s are the values that go into the interpolation function
        s = (mid - minimum) / (maximum - minimum)
        return minimum + (maximum - minimum) * self.InterpolationFunction(p / 100, s)

    @commands.command()
    async def gearcalc(
        self, ctx, ability=None, AP="", AdditionalInput="", AdditionalInput2=""
    ):
        if ability == None:
            await ctx.send("Error: No ability entered.")
        elif ability == "help":
            if AP in self.abilitydict and AP != "":
                if AP == "mpu":
                    await ctx.send(
                        "Calculates the effects of Main Power Up on a certain weapon. Usage: `a.gearcalc mpu (amount) (weapon)`. Use `a.weaponglossary` for a list of valid weapon names."
                    )
                elif AP == "spu":
                    await ctx.send(
                        "Calculates the effects of Special Power Up on a certain special. Usage: `a.gearcalc spu (amount) (special)`. Use `a.subspecialglossary` for a list of valid special weapon names."
                    )
                elif AP == "bpu":
                    await ctx.send(
                        "Calculates the effects of sub power up on a given sub weapon. Usage: `a.gearcalc bpu (amount) (sub)`. Use `a.subspecialglossary` for a list of valid sub weapon names."
                    )
                elif AP == "res":
                    await ctx.send(
                        "Calculates the effects of Ink Resistance Up. Can be modified by Opening Gambit. Usage: `a.gearcalc res (amount) [og]`."
                    )
                elif AP == "bdx" or AP == "bdef":
                    await ctx.send(
                        "Calculates the effects of Bomb Defense Up. Usage: `a.gearcalc bdx (amount)`or `a.gearcalc bdef (amount)`."
                    )
                elif AP == "rec" or AP == "iru":
                    await ctx.send(
                        "Calculates the effects of Ink Recovery Up. Can be modified by Comeback or Last-Ditch Effort and/or if given weapon is the Splattershot Jr. Usage: `a.gearcalc res (amount) [cbk/lde] [jr]`."
                    )
                elif AP == "scu":
                    await ctx.send(
                        "Calculates the special cost given the original special cost. Can be modified by Comeback. Usage: `a.gearcalc scu (amount) (original special cost) [cbk]`."
                    )
                elif AP == "ss":
                    await ctx.send(
                        "Calculates the percentage of the special meter saved. Usage: `a.gearcalc scu (amount)."
                    )
                elif AP == "iss":
                    await ctx.send(
                        "Calculates the percentage of the ink tank consumed by a sub weapon. Can be modified by Comeback and Last Ditch Effort. Usage: `a.gearcalc (amount) (sub weapon) [cbk/lde]`. Use `a.subspecialglossary` for a list of valid sub weapon names."
                    )
                elif AP == "ism":
                    await ctx.send(
                        "Calculates the effects of Ink Saver Main given a weapon. Can be modified by Comeback or Last-Ditch Effort. Usage: `a.gearcalc ism (amount) (weapon) [cbk/lde]`."
                    )
                elif AP == "rsu":
                    await ctx.send(
                        "Calculates the effects of Run Speed Up given a weapon. Can be modified by Comeback and Opening Gambit. Usage: `a.gearcalc rsu (amount) (weapon) [cbk/og]`."
                    )
                elif AP == "ssu":
                    await ctx.send(
                        "Calculates the effect of Swim Speed Up given a weight class. Can be modified Comeback, Opening Gambit and Ninja Squid. Weight classes are 'lightweight', 'middleweight', 'heavyweight', and 'rainmaker'. Usage: `a.gearcalc ssu (amount) (weight class) [cbk/og/ns]`."
                    )
                elif AP == "qsj":
                    await ctx.send(
                        "Calculates the effects of Quick Super Jump. Usage: `a.gearcalc qsj (amount)`."
                    )
                elif AP == "qr":
                    await ctx.send(
                        "Calculates the effects of Quick Respawn. Usage: 'a.gearcalc qr (amount)`.'"
                    )
                else:
                    await ctx.send(
                        "Invalid ability entered. Use 'a.abilityglossary' for accepted ability names."
                    )
            else:
                await ctx.send(
                    "The `gearcalc` command calculates the effects of an amount of an ability inputted. Usage: `a.gearcalc (ability) (amount) [modifier if applicable] [modifier if applicable]`. Amount must be in 0m0s format. Example: 1m2s, for 1 main 2 subs.\n Use `a.weaponglossary` for accepted weapon names, `a.abilityglossary` for accepted ability names and `a.subspecialglossary` for accepted sub and special weapon names."
                )
        # elif AP == "0m0s":
        # await ctx.send("Error! Invalid ability amount entered. Amount must be in 0m0s format. Example: 1m2s, for 1 main 2 subs.")
        elif (
            ability == "spu" or ability == "bpu" or ability == "mpu" or ability == "res"
        ):
            # try:
            await ctx.send(self.abilitydict[ability](ctx, AP, AdditionalInput))
        # except:
        # await ctx.send("Error: Invalid ability or ability amount entered. Use `a.gearcalc help` for formatting help.")
        elif (
            ability == "ssu"
            or ability == "iss"
            or ability == "ism"
            or ability == "rsu"
            or ability == "scu"
            or ability == "rec"
            or ability == "iru"
        ):
            try:
                await ctx.send(
                    self.abilitydict[ability](
                        ctx, AP, AdditionalInput, AdditionalInput2
                    )
                )
            except:
                await ctx.send(
                    "Error: Invalid ability or ability amount entered. Use `a.gearcalc help` for formatting help."
                )
        else:
            # await ctx.send(self.abilitydict[ability])
            try:
                await ctx.send(self.abilitydict[ability](ctx, AP))
            except:
                await ctx.send(
                    "Error: Invalid ability or ability amount entered. Use `a.gearcalc help` for formatting help."
                )
            # else, try calling a gearcalc function by ability name entered , if no such ability exists, throw an error

    def calcbdef(self, ctx, AP):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        bombs = {
            "Splat Bomb (near)": 180,
            "Splat Bomb (far)": 30,
            "Suction Bomb (near)": 180,
            "Suction Bomb (far)": 30,
            "Autobomb (near)": 150,
            "Autobomb (far)": 30,
            "Curling Bomb (near)": 150,
            "Curling Bomb (far)": 30,
            "Burst Bomb (direct)": 60,
            "Burst Bomb (near)": 35,
            "Burst Bomb (far)": 25,
            "Ink Mine (near)": 45,
            "Ink Mine (far)": 35,
            "Torpedo (near)": 60,
            "Torpedo (far)": 35,
            "Torpedo (droplets)": 12,
        }

        specials = {
            "Tenta missiles (hit)": [150, 100],
            "Tenta missiles (near)": [50, 32.5],
            "Tenta missiles (far)": [30, 19.5],
            "Baller (hit)": [50, 32.5],
            "Baller (near)": [180, 100],
            "Baller (far)": [55, 35.8],
            "Splashdown (hit)": [180, 100],
            "Splashdown (near)": [70, 45.5],
            "Splashdown (far)": [55, 35.8],
            "Inkjet (hit)": [120, 100],
            "Inkjet (near)": [50, 32.5],
            "Inkjet (far)": [30, 19.5],
        }
        amnt = 0.99 * AP - (0.09 * AP) ** 2
        results = {}
        for bomb in bombs.keys():
            if "Burst Bomb" in bomb:
                results[bomb] = bombs[bomb] * (1 - amnt / 75)
            else:
                if bombs[bomb] * (1 - amnt / 60) < 100 and (
                    bomb == "Splat Bomb (near)"
                    or bomb == "Suction Bomb (near)"
                    or bomb == "Autobomb (near)"
                    or bomb == "Curling Bomb (near)"
                ):
                    results[bomb] = 100
                else:
                    results[bomb] = bombs[bomb] * (1 - amnt / 60)

        end = "Damage done by sub weapons:\n"
        for result in results.keys():
            end += f"{result}: {round(results[result], 2)} ({round(results[result] - bombs[result], 2)})\n"

        special_damages = []
        for special in specials.keys():
            damage = round(
                self.calcAbilityEffects(AP, specials[special][0], specials[special][1]),
                2,
            )
            if damage < 100 and (
                special == "Tenta Missiles (hit)"
                or special == "Baller (hit)"
                or special == "Splashdown (hit)"
                or special == "Inkjet (hit)"
            ):
                damage = 100
            special_damages.append(damage)

        special_names = list(specials.keys())
        end += "\nDamage done by specials:\n"
        for x in range(11):
            end += f"{special_names[x]}: {special_damages[x]}\n"

        SensorTrackingTime = self.calcAbilityEffects(AP, 8, 0.8)
        pctchange1 = round(self.calcPctChange(8, SensorTrackingTime), 2)
        MineTrackingTime = self.calcAbilityEffects(AP, 5, 0.5)
        pctchange2 = round(self.calcPctChange(5, MineTrackingTime), 2)
        end += f"\nTracking times:\nPoint sensor tracking time: {round(SensorTrackingTime,2)} seconds ({pctchange1}% change).\nInk mine tracking time: {round(MineTrackingTime,2)} seconds ({pctchange2}% change).\n"
        return end

    # calculates the special cost given a number of ability points and the original special cost
    def calcscu(self, ctx, AP, SpecialCostInput, modifier=""):
        if modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        SpecialCost = float(SpecialCostInput)
        NewSpecialCost = SpecialCost / (1 + (0.99 * AP - (0.09 * AP) ** 2) / 100)
        PercentChange = self.calcPctChange(SpecialCost, NewSpecialCost)
        return "Special Cost: {}p, {}% change.".format(
            round(NewSpecialCost, 2), round(PercentChange, 2)
        )

    def calcrec(
        self, ctx, AP, modifier="", jr=""
    ):  # calculates time to recover ink tank given an amount of ability points
        if modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        elif modifier == "last-ditch-effort" or modifier == "lde":
            AP = self.calcAP(AP) + 24
        else:
            AP = self.calcAP(AP)
        if AP > 57:  # to avoid AP values going over the maximum possible in game
            AP = 57
        if modifier == "jr" or jr == "jr":
            kid = self.calcAbilityEffects(
                AP, 11, 4.05
            )  # (time to recover ink in squid/kid form in frames * percentage of that respective form in inkipedia) / 60 (because it's frames) -c
            squid = self.calcAbilityEffects(AP, 3.32, 2.15)
        else:
            kid = self.calcAbilityEffects(
                AP, 10, 3.67
            )  # units in seconds to recover ink tank fully
            squid = self.calcAbilityEffects(AP, 3, 1.95)
        kidpctchange = self.calcPctChange(10, kid)
        squidpctchange = self.calcPctChange(3, squid)
        # return f"modifier: {modifier}. jr: {jr}. squid: {squid}. kid: {kid}. kid & squid pct change: {kidpctchange}, {squidpctchange}"
        return f"Full tank recovery time: {round(kid, 2)} seconds out of ink ({round(kidpctchange, 2)}% change), {round(squid, 2)} seconds submerged in ink ({round(squidpctchange, 2)}% change)"

    def calcinkres(
        self, ctx, AP, OpeningGambit=""
    ):  # calculates the effects of ink resistance given an amount of ability points
        if OpeningGambit == "opening-gambit" or OpeningGambit == "og":
            AP = self.calcAP(AP) + 30
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        RunSpeedEnemyInk = self.calcAbilityEffects(AP, 0.24, 0.768)  # units: DU/F
        DamagePerSecond = self.calcAbilityEffects(AP, 18, 9)  # Units: hp/s
        DamageLimit = self.calcAbilityEffects(AP, 40, 20)  # units: hp
        InvinsTime = self.calcAbilityEffects(AP, 0, 0.65)  # units: seconds
        JumpHeight = self.calcAbilityEffects(AP, 0.8, 1.1)
        pctchange = round(self.calcPctChange(0.24, RunSpeedEnemyInk), 2)
        pctchange2 = round(self.calcPctChange(18, DamagePerSecond), 2)
        pctchange3 = round(self.calcPctChange(40, DamageLimit), 2)
        pctchange4 = round(
            self.calcPctChange(0.8, JumpHeight), 2
        )  # no %change for invulnerability time because of a division by 0 error
        return f"Run speed in enemy ink: {round(RunSpeedEnemyInk, 2)} distance units per frame ({pctchange}% change).\nDamage per second in enemy ink: {round(DamagePerSecond,2)} hp ({pctchange2}% change).\nDamage limit in enemy ink: {round(DamageLimit,2)} hp ({pctchange3}% change).\nInvulnerability time in enemy ink: {round(InvinsTime,2)} seconds.\nJump height in enemy ink: {round(JumpHeight,2)} ({pctchange4}% change)."

    def calcqr(self, ctx, AP):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        RespawnTime = self.calcAbilityEffects(AP, 8.5, 4.5)
        pctchange = round(self.calcPctChange(8.5, RespawnTime))
        return f"Respawn time: {round(RespawnTime, 2)} seconds ({pctchange}% change)."

    def calcqsj(self, ctx, AP):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        kid = round(
            self.calcAbilityEffects(AP, 3.98, 2.29), 2
        )  # separate variables for readability
        squid = round(self.calcAbilityEffects(AP, 3.63, 1.94), 2)
        return f"Super Jump Time: {kid} seconds in kid form, {squid} in squid form"

    def calcspu(self, ctx, AP, specialtype):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        specials = [
            "baller",
            "curling-launcher",
            "suction-launcher",
            "splat-launcher",
            "autobomb-launcher",
            "burst-launcher",
            "booyah",
            "bubbles",
            "inkjet",
            "armor",
            "storm",
            "rain",
            "missiles",
            "ray",
            "stamp",
            "splashdown",
        ]  # rain and storm are the same thing both are used commonly enough that it makes sense to have both
        if specialtype not in specials:
            return "Error: Invalid special type entered."
        else:
            if specialtype == "baller":
                hp = 400 * (1 + (0.99 * AP - (0.09 * AP) ** 2) / 60)
                pctchange = self.calcPctChange(400, hp)
                return f"Baller HP: {round(hp, 2)}. Change from base HP of 400: {round(hp - 400, 2)} ({round(pctchange, 2)}% change)."
            elif specialtype == "armor":
                ActivationTime = self.calcAbilityEffects(
                    AP, 1.5, 0.5
                )  # units are seconds
                Duration = self.calcAbilityEffects(AP, 6, 9)
                pctchange1 = self.calcPctChange(1.5, ActivationTime)
                # pctchange2 = self.calcPctChange(6, ActivationTime) this is sptting out weird values so it's being removed for now
                return f"Armor activation time {round(ActivationTime,2)} seconds ({round(pctchange1,2)}% change). Armor duration: {round(Duration,2)} seconds."
            elif specialtype == "splashdown":
                diameter = 2.8 * (1 + (0.99 * AP - (0.09 * AP) ** 2) / 110)
                return f"Splashdown effective diameter in testing room lines: {round(diameter, 2)}."
            elif specialtype == "ray":
                RayDuration = self.calcAbilityEffects(
                    AP, 7.75, 9.75
                )  # units are seconds
                pctchange = self.calcPctChange(7.75, RayDuration)
                return f"Sting Ray Duration: {round(RayDuration,2)} seconds, increase of {round(RayDuration - 7.75, 2)} from base duration of 7.75 seconds ({round(pctchange,2)}% change)."
            elif specialtype == "inkjet":
                duration = self.calcAbilityEffects(AP, 7.5, 8.5)  # units are seconds
                pctchange = round(self.calcPctChange(7.5, duration))
                return f"Duration: {round(duration, 2)} seconds ({pctchange}% change)."
            elif (
                specialtype == "suction-launcher"
                or specialtype == "splat-launcher"
                or specialtype == "burst-launcher"
                or specialtype == "autobomb-launcher"
            ):
                duration = self.calcAbilityEffects(AP, 6, 8)  # units in seconds
                pctchange = round(self.calcPctChange(6, duration))
                return f"Bomb launcher duration: {round(duration,2)} seconds ({pctchange}% change)."
            elif specialtype == "curling-launcher":
                duration = self.calcAbilityEffects(AP, 6.67, 8.67)
                pctchange = round(self.calcPctChange(6.67, duration))
                return f"Bomb launcher duration {round(duration,2)} seconds ({pctchange}% change)."
            elif specialtype == "booyah":
                ChargeTime = self.calcAbilityEffects(
                    AP, 8.483, 8.415
                )  # units are seconds
                pctchange = self.calcPctChange(8.483, ChargeTime)
                return f"Maximum Booyah Bomb charge time: {round(ChargeTime,2)} seconds ({round(pctchange,2)}% change)"
            elif specialtype == "bubbles":
                BubbleRadius = self.calcAbilityEffects(AP, 30, 39)
                pctchange = self.calcPctChange(30, BubbleRadius)
                return f"Maximum bubble radius: {round(BubbleRadius, 2)} ({round(pctchange,2)}% change)."
            elif specialtype == "storm" or specialtype == "rain":  # missing throw range
                StormDuration = self.calcAbilityEffects(AP, 8, 10)  # units are seconds
                pctchange = self.calcPctChange(8, StormDuration)
                return f"Inkstorm duration: {round(StormDuration,2)} seconds ({round(pctchange,2)}% change)."
            elif specialtype == "stamp":
                Duration = self.calcAbilityEffects(AP, 9, 11)
                pctchange = self.calcPctChange(9, Duration)
                return f"Ultra Stamp duration: {round(Duration,2)} seconds ({round(pctchange,2)}% change)."
            elif specialtype == "missiles":
                TargetingRadius = self.calcAbilityEffects(AP, 140, 240)
                pctchange = self.calcPctChange(140, TargetingRadius)
                InkCoverageIncrease = (
                    self.calcAbilityEffects(AP, 100, 120) - 100
                )  # units are a percentage
                return f"Tenta Missiles targeting radius: {round(TargetingRadius,2)} ({round(pctchange,2)}% change). Increase in ink coverage: {round(InkCoverageIncrease,2)}%."
            else:
                return "No data yet, check back later."

    def calcssu(
        self, ctx, AP, weightclass, modifier=""
    ):  # calculates swim speed given an amount of ability chunks, the weapon's weight class and another modifier like ninja squid if applicable
        if modifier == "opening-gambit" or modifier == "og":
            AP = self.calcAP(AP) + 30
        elif modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57

        if weightclass == "lightweight":
            swimspeed = self.calcAbilityEffects(AP, 2.016, 2.4)
            if modifier == "ninja-squid" or modifier == "ns":
                swimspeed = swimspeed * 0.9
            percentchange = self.calcPctChange(2.016, swimspeed)
        elif weightclass == "middleweight":
            swimspeed = self.calcAbilityEffects(AP, 1.92, 2.4)
            if modifier == "ninja-squid" or modifier == "ns":
                swimspeed = swimspeed * 0.9
            percentchange = self.calcPctChange(1.92, swimspeed)
        elif weightclass == "heavyweight":
            swimspeed = self.calcAbilityEffects(AP, 1.728, 2.4)
            if modifier == "ninja-squid" or modifier == "ns":
                swimspeed = swimspeed * 0.9
            percentchange = self.calcPctChange(1.728, swimspeed)
        elif weightclass == "rainmaker" or modifier == "ns":
            swimspeed = self.calcAbilityEffects(AP, 1.92, 2.4) * 0.8
            if modifier == "ninja-squid":
                swimspeed = swimspeed * 0.9
            percentchange = self.calcPctChange(1.92, swimspeed)

        return f"Swim speed: {round(swimspeed, 2)} distance units per frame, {round(percentchange,2)}% increase"

    def calcrsu(
        self, ctx, AP, weapon, modifier=""
    ):  # calculates the user's run speed given an amount of ability chunk and weapon weight class
        if modifier == "opening-gambit" or modifier == "og":
            AP = self.calcAP(AP) + 30
        elif modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57

        StrafingSpeeds = {  # measured in distance units per second
            "sploosh": [0.8, 1.0],
            "splash": [0.72, 0.9],
            "jr": [0.72, 0.9],
            "splattershot": [0.72, 0.9],
            "aerospray": [0.72, 0.9],
            "l-3": [0.8, 1.0],
            "52": [0.6, 0.75],
            "pro": [0.55, 0.6875],
            "96": [0.4, 0.5],
            "jet": [0.6, 0.75],
            "squeezer": [0.72, 0.9],
            "h-3": [0.6, 0.75],
            "luna": [0.5, 0.625],
            "blaster": [0.45, 0.5625],
            "range-blaster": [0.4, 0.5],
            "clash": [0.65, 0.8125],
            "rapid-blaster": [0.55, 0.6875],
            "rapid-pro": [0.5, 0.625],
            "squiffer": [0.3, 0.375],
            "charger": [0.2, 0.25],
            "scope": [0.2, 0.25],
            "eliter": [0.15, 0.1875],
            "eliter-scope": [0.15, 0.1875],
            "bamboozler": [0.6, 0.75],
            "gootuber": [0.3, 0.375],
            "slosher": [0.4, 0.5],
            "tri": [0.66, 0.825],
            "machine": [0.7, 0.875],
            "explosher": [0.45, 0.5625],
            "bloblobber": [0.5, 0.625],
            "mini": [0.865, 1.211],
            "heavy": [0.7, 0.945],
            "hydra": [0.6, 0.81],
            "nautilus": [0.7, 0.91],
            "ballpoint": [0.86, 1.07],
            "dapples": [0.8, 1.0],
            "dualies": [0.8, 1.0],
            "dualie-squelchers": [0.72, 0.9],
            "gloogas": [0.6, 0.75],
            "tetras": [0.72, 0.9],
            "brella": [0.65, 0.8125],
            "undercover": [0.72, 0.9],
            "tent": [0.5, 0.625],
        }
        NoStrafingSpeedWeapons = [
            "roller",
            "carbon",
            "dynamo",
            "flingza",
            "rainmaker",
            "inkbrush",
            "octobrush",
        ]
        if (
            weapon == "hydra"
            or weapon == "dynamo"
            or weapon == "eliter"
            or weapon == "eliter-scope"
            or weapon == "explosher"
            or weapon == "tent"
            or weapon == "hydra"
        ):
            weightclass = "heavyweight"
        elif (
            weapon == "aerospray"
            or weapon == "bamboozler"
            or weapon == "carbon"
            or weapon == "clash"
            or weapon == "jr"
            or weapon == "inkbrush"
            or weapon == "luna"
            or weapon == "nzap"
            or weapon == "splash"
            or weapon == "sploosh"
            or weapon == "tri"
            or weapon == "undercover"
        ):
            weightclass = "lightweight"
        else:
            weightclass = "middleweight"

        if weightclass == "lightweight":
            runspeed = self.calcAbilityEffects(AP, 1.04, 1.44)
            percentchange = self.calcPctChange(1.04, runspeed)
        elif weightclass == "middleweight":
            runspeed = self.calcAbilityEffects(AP, 0.96, 1.44)
            percentchange = self.calcPctChange(0.96, runspeed)
        elif weightclass == "heavyweight":
            runspeed = self.calcAbilityEffects(AP, 0.88, 1.44)
            percentchange = self.calcPctChange(1.728, runspeed)
        elif weapon == "rainmaker":
            runspeed = self.calcAbilityEffects(AP, 0.96, 1.44) * 0.8
            percentchange = self.calcPctChange(0.96, runspeed)

        if weapon in NoStrafingSpeedWeapons:
            return f"Run speed: {round(runspeed, 2)} distance units per frame, {round(percentchange,2)}% increase."
        elif weapon in list(StrafingSpeeds.keys()):
            StrafeSpeed = self.calcAbilityEffects(
                AP, StrafingSpeeds[weapon][0], StrafingSpeeds[weapon][1]
            )
            pctchange2 = round(
                self.calcPctChange(StrafingSpeeds[weapon][0], StrafeSpeed), 2
            )
            return f"Run speed: {round(runspeed, 2)} distance units per frame, {round(percentchange,2)}% change. Run speed while firing: {round(StrafeSpeed,2)} distance units per frame ({pctchange2}% change)."
        else:
            return "Invalid weapon name entered. Use a.weaponglossary for a list of weapon names."

    def calcss(self, ctx, AP):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        SpecialSaved = round(self.calcAbilityEffects(AP, 50.00, 100.00, 80.00), 2)
        return f"Special charge kept after death: {SpecialSaved}%"

    def calcbpu(self, ctx, AP, SubType):
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        SubWeapons = [
            "splat-bomb",
            "burst-bomb",
            "suction-bomb",
            "autobomb",
            "curling-bomb",
            "mine",
            "beakon",
            "fizzy-bomb",
            "toxic-mist",
            "wall",
            "sprinkler",
            "torpedo",
            "sensor",
        ]
        if SubType in SubWeapons:
            if (
                SubType == "splat-bomb"
                or SubType == "burst-bomb"
                or SubType == "autobomb"
                or SubType == "curling-bomb"
                or SubType == "toxic-mist"
                or SubType == "suction-bomb"
            ):
                ThrowRange = self.calcAbilityEffects(AP, 11.2, 16.8)
                pctchange = round(self.calcPctChange(11.2, ThrowRange), 2)
                return f"Bomb range: {round(ThrowRange,2)} ({pctchange}% change)"
            elif SubType == "torpedo" or SubType == "fizzy-bomb":
                ThrowRange = self.calcAbilityEffects(AP, 13.6, 18.4)
                pctchange = round(self.calcPctChange(13.6, ThrowRange), 2)
                return f"Bomb range: {round(ThrowRange,2)} ({pctchange}% change)"
            elif SubType == "sprinkler":
                Duration = self.calcAbilityEffects(AP, 20, 27)  # units in seconds
                pctchange = round(self.calcPctChange(20, Duration), 2)
                return f"Sprinkler duration: {round(Duration,2)} seconds ({pctchange}% change)"
            elif SubType == "wall":
                WallHP = self.calcAbilityEffects(AP, 800, 1500)  # units in hp
                pctchange = round(self.calcPctChange(800, WallHP), 2)
                return f"Wall HP: {round(WallHP,2)} ({pctchange}% change)"
            elif SubType == "mine":
                BlastRadius = self.calcAbilityEffects(AP, 100, 137.5)  # measured in %
                TrackingTime = self.calcAbilityEffects(AP, 5, 10)  # measured in seconds
                pctchange = round(self.calcPctChange(5, TrackingTime), 2)
                return f"Mine blast radius: {round(BlastRadius,2)}% of base radius. Mine tracking time: {round(TrackingTime,2)} seconds ({pctchange}% change)."
            elif SubType == "beakon":
                JumpTime = self.calcAbilityEffects(AP, 3.63, 1.94)
                pctchange = round(self.calcPctChange(3.63, JumpTime), 2)
                return f"Jump time to beakon (without Quick Super Jump): {round(JumpTime,2)} seconds ({pctchange}% change)"
            elif SubType == "sensor":
                SensorRange = self.calcAbilityEffects(AP, 13.8, 18.7)
                pctchange1 = round(self.calcPctChange(13.8, SensorRange), 2)
                TrackingTime = self.calcAbilityEffects(AP, 8, 16)  # measured in seconds
                pctchange2 = round(self.calcPctChange(8, TrackingTime), 2)
                return f"Point Sensor range: {round(SensorRange,2)} ({pctchange1}% change). Tracking time: {round(TrackingTime,2)} seconds ({pctchange2}% change)."
            else:
                return "Error: invalid sub weapon or number of chunks entered."
        else:
            return "Error: invalid sub weapon name entered. Accepted names: splat-bomb, curling-bomb, burst-bomb, autobomb, suction-bomb, fizzy-bomb, torpedo, beakon, wall, sprinkler, sensor, toxic-mist, mine."

    def calciss(self, ctx, AP, SubType, modifier=""):  # modifiers are lde and comeback
        SubWeapons = {
            "splat-bomb": [70, 45.5],  # units in % of ink tank used
            "burst-bomb": [40, 32],
            "suction-bomb": [70, 45.5],
            "autobomb": [55, 38.5],
            "curling-bomb": [70, 45.5],
            "fizzy-bomb": [60, 42],
            "torpedo": [65, 42.25],
            "toxic-mist": [60, 42],
            "sensor": [45, 31.5],
            "mine": [60, 36],
            "wall": [60, 39],
            "sprinkler": [60, 36],
            "beakon": [75, 45],
        }
        if modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        elif modifier == "last-ditch-effort" or modifier == "lde":
            AP = self.calcAP(AP) + 24
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57

        SubCost = self.calcAbilityEffects(
            AP, SubWeapons[SubType][0], SubWeapons[SubType][1]
        )
        NumberBombs = int(100 / SubCost)
        output = (
            f"Sub weapon cost: {round(SubCost, 2)}% of ink tank, {NumberBombs} bomb(s)."
        )
        if SubType == "splat-bomb" or SubType == "autobomb" or SubType == "torpedo":
            SubCostsJr = {
                "splat-bomb": [63.63636, 41.36364],
                "autobomb": [50, 35],
                "torpedo": [59.09091, 38.40909],
            }
            SubCostJr = self.calcAbilityEffects(
                AP, SubCostsJr[SubType][0], SubCostsJr[SubType][1]
            )
            output += f" {round(SubCostJr, 2)}% of ink tank, {int(100/SubCostJr)} bombs with Splattershot Jr."
        return output

    def calcism(self, ctx, AP, weapon, modifier=""):
        if modifier == "comeback" or modifier == "cbk":
            AP = self.calcAP(AP) + 10
        elif modifier == "last-ditch-effort" or modifier == "lde":
            AP = self.calcAP(AP) + 24
        else:
            AP = self.calcAP(AP)
        if AP > 57:
            AP = 57
        weapons = {
            "jr": 0.43,
            "aerospray": 0.55,
            "nzap": 0.8,
            "splash": 0.8,
            "dualies": 0.722,
            "sploosh": 0.9,
            "dapples": 0.665,
            "tetras": 0.8,
            "squeezer": [1.08, 2.2],  # tap ,hold
            "splattershot": 0.92,
            "dualie-squelchers": 1.2,
            "l-3": [1.15, 3.45],
            "gloogas": 1.4,
            "52": 1.15,
            "jet": 1.6,
            "h-3": [2.25, 6.75],  # individual shot , zr tap
            "pro": 2,
            "96": 2.5,
            "inkbrush": 2,
            "octobrush": 3.2,
            "carbon": 4,
            "flingza": [8, 12],  # horizontal ,vertical
            "roller": 9,
            "dynamo": 18,
            "clash": 4,
            "undercover": 4,
            "brella": 6.35,
            "tri": 6,
            "rapid-blaster": 7,
            "slosher": 7,
            "bloblobber": 8,
            "machine": 8.4,
            "rapid-pro": 8,
            "luna ": 7.5,
            "tent": 11,
            "blaster": 10,
            "range-blaster": 11,
            "explosher": 11.7,
            "bamboozler": 8.4,
            "squiffer": 10.5,
            "gootuber": 15,
            "nautilus": 15,
            "mini": 17.25,
            "charger": 18,
            "heavy": 22.5,
            "eliter": 25,
            "ballpoint": 25,
            "hydra": 35,
        }
        highink = ["dynamo", "eliter", "h-3", "hydra", "luna", "pro", "tent"]
        chargers = [
            "bamboozler",
            "squiffer",
            "gootuber",
            "nautilus",
            "mini",
            "charger",
            "heavy",
            "eliter",
            "ballpoint",
            "hydra",
        ]
        if weapon not in list(weapons.keys()):
            return "Invalid weapon name entered. Use `a.weaponglossary` for a list of weapon names."
        elif weapon in highink:
            percdif = (0.99 * AP - (0.09 * AP) ** 2) / 60
        else:
            percdif = (0.99 * AP - (0.09 * AP) ** 2) / (200 / 3)
        if (
            weapon == "flingza"
            or weapon == "squeezer"
            or weapon == "l-3"
            or weapon == "h-3"
        ):
            inkcons1 = weapons[weapon][0] * (1 - percdif)
            shots1 = int(100 / inkcons1)
            inkcons2 = weapons[weapon][1] * (1 - percdif)
            shots2 = int(100 / inkcons2)
        elif weapon == "jr":
            inkcons = weapons[weapon] * (1 - percdif)
            shots = int((100 / inkcons) * 1.1)
        else:
            inkcons = weapons[weapon] * (1 - percdif)
            shots = int(100 / inkcons)
        if weapon == "flingza":
            return f"Number of horizontal flicks with {weapon}: {shots1}. Number of vertical flicks: {shots2}."
        elif weapon == "squeezer":
            return f"Number of auto shots with {weapon}: {shots1}. Number of tap shots: {shots2}."
        elif weapon == "l-3" or weapon == "h-3":
            return f"Number of individual shots with {weapon}: {shots1}. Number of full bursts: {shots2}."
        elif "brush" in weapon or weapon in ["carbon", "roller", "dynamo"]:
            return f"Number of flicks with {weapon}: {shots}."
        elif weapon in chargers:
            return f"Number of full charges with {weapon}: {shots}."
        else:
            return f"Number of shots with {weapon}: {shots}."

    def calcmpu(self, ctx, AP, Weapon):
        DamageBuffWeapons = {
            "sploosh": [38, 47.5],  # units in damage dealt
            "splash": [28, 33.3],
            "pro": [42, 49.9],
            "96": [62, 77.5],
            "l-3": [29, 33.3],
            "h-3": [41, 49.9],
            "squeezer": [38, 49.4],
            "dapples": [36, 43.2],
            "dualies": [30, 33.3],
            "dualie-squelchers": [28, 33.3],
            "tetras": [28, 33.3],
            "ballpoint": [28, 30.8],
        }
        PaintingBuffWeapons = {  # units are percent ink coverage from base value
            "jr": [100, 120.155],
            "aerospray": [100, 116.667],
            "tri": [100, 120],
            "machine": [100, 115],
            "bloblobber": [100, 120],
            "explosher": [100, 130],
        }
        NonTentBrellas = {  # units are seconds to regenerate canopy
            "brella": [6.5, 3.5],
            "undercover": [4.5, 2.5],
        }
        HeavyNautMini = {
            "heavy": [
                1.2,
                1.49,
                2.4,
                2.98,
            ],  # units are seconds, with the minimum and maximum first and second ring burst duration
            "nautilus": [0.87, 1.13, 1.73, 2.25],
            "mini": [0.6, 0.81, 1.2, 1.62],
        }
        Brushes = {
            "inkbrush": [
                1.92,
                2.016,
                100,
                148,
            ],  # units are dash speed in DU/frame and % trail ink coverage from base value
            "octobrush": [1.68, 1.8816, 100, 180],
        }
        SquifferEliter = {
            "eliter": [
                290.5,
                305.5,
                100,
                117,
            ],  # units are max range and percent ink coverage from base value
            "eliter-scope": [310.5, 325.5, 100, 117],
            "squiffer": [167.65, 182.65, 100, 124],
        }
        ChargerGooBamboo = {
            "charger": [
                40,
                48,
                80,
                96,
            ],  # units are the damage at min partial charge and max partial charge
            "scope": [40, 48, 80, 96],
            "gootuber": [40, 46, 130, 149.5],
            "bamboozler": [30, 36, 85, 99.9],
        }
        Shot52 = {
            "splattershot": [
                100,
                50,
                100,
                80,
            ],  # units are percentage of base value of jump and ground shot randomization
            "52": [100, 50, 100, 80],
        }
        BlasterRangeClash = {
            "blaster": [
                100,
                60,
            ],  # units are percentage of base value of jump shot randomization
            "range-blaster": [100, 62.5],
            "clash": [100, 50],
        }
        Rollers = {
            "roller": [
                100,
                115,
            ],  # units are % of base value of damage for now since mpu effects for roller seem to differ between gear calculators
            "carbon": [100, 115],
            "flingza": [100, 115],
            "dynamo": [100, 115],
        }
        # all other mpu effects are weapon specific and will be defined in if statements
        AP = self.calcAP(AP)
        if AP > 57:
            AP = 57

        if Weapon in list(DamageBuffWeapons.keys()):
            Damage = self.calcAbilityEffects(
                AP, DamageBuffWeapons[Weapon][0], DamageBuffWeapons[Weapon][1]
            )
            pctchange = round(
                self.calcPctChange(DamageBuffWeapons[Weapon][0], Damage), 2
            )
            return f"Weapon damage: {round(Damage, 1)} ({pctchange}% change)."
        elif Weapon in list(PaintingBuffWeapons.keys()):
            Painting = self.calcAbilityEffects(
                AP, PaintingBuffWeapons[Weapon][0], PaintingBuffWeapons[Weapon][1]
            )
            return f"Painting ability: {round(Painting,2)}% of base painting ability."
        elif Weapon in list(NonTentBrellas.keys()):
            CanopyRegenTime = self.calcAbilityEffects(
                AP, NonTentBrellas[Weapon][0], NonTentBrellas[Weapon][1]
            )
            pctchange = round(
                self.calcPctChange(NonTentBrellas[Weapon][0], CanopyRegenTime), 2
            )
            return f"Canopy regeneration time: {round(CanopyRegenTime,2)} seconds ({pctchange}% change)."
        elif Weapon in list(
            HeavyNautMini.keys()
        ):  # can you check this line i can't see anything wrong - quark --done -c
            RingBurstTime1 = self.calcAbilityEffects(
                AP, HeavyNautMini[Weapon][0], HeavyNautMini[Weapon][1]
            )
            pctchange1 = round(
                self.calcPctChange(HeavyNautMini[Weapon][0], RingBurstTime1), 2
            )
            RingBurstTime2 = self.calcAbilityEffects(
                AP, HeavyNautMini[Weapon][2], HeavyNautMini[Weapon][3]
            )
            pctchange2 = round(
                self.calcPctChange(HeavyNautMini[Weapon][2], RingBurstTime2), 2
            )
            return f"First ring burst duration: {round(RingBurstTime2,2)} seconds ({pctchange1}% change). Second ring burst duration: {round(RingBurstTime2,2)} seconds ({pctchange2}% change)."
        elif Weapon in list(Brushes.keys()):
            DashSpeed = self.calcAbilityEffects(
                AP, Brushes[Weapon][0], Brushes[Weapon][1]
            )
            pctchange1 = round(self.calcPctChange(Brushes[Weapon][0], DashSpeed), 2)
            InkTrailSize = round(
                self.calcAbilityEffects(AP, Brushes[Weapon][2], Brushes[Weapon][3]), 2
            )
            return f"Dash speed: {round(DashSpeed,2)} distance units per second ({pctchange1}% change). Ink trail size {InkTrailSize}% of base size."
        elif Weapon in list(SquifferEliter.keys()):
            MaxRange = self.calcAbilityEffects(
                AP, SquifferEliter[Weapon][0], SquifferEliter[Weapon][1]
            )
            pctchange = round(
                self.calcPctChange(SquifferEliter[Weapon][0], MaxRange), 2
            )
            Painting = round(
                self.calcAbilityEffects(
                    AP, SquifferEliter[Weapon][2], SquifferEliter[Weapon][3]
                ),
                2,
            )
            return f"Maximum range: {round(MaxRange,2)} ({pctchange}% change). Painting ability: {Painting}% of base paint output."
        elif Weapon in list(ChargerGooBamboo.keys()):
            MinChargeDamage = self.calcAbilityEffects(
                AP, ChargerGooBamboo[Weapon][0], ChargerGooBamboo[Weapon][1]
            )
            pctchange1 = round(
                self.calcPctChange(ChargerGooBamboo[Weapon][0], MinChargeDamage), 2
            )
            MaxPartialChargeDamage = self.calcAbilityEffects(
                AP, ChargerGooBamboo[Weapon][2], ChargerGooBamboo[Weapon][3]
            )
            pctchange2 = round(
                self.calcPctChange(ChargerGooBamboo[Weapon][2], MaxPartialChargeDamage)
            )
            return f"Damage at minimum charge: {round(MinChargeDamage,2)} ({pctchange1}% change). Damage at maximum partial charge (or full charge for bamboo): {round(MaxPartialChargeDamage,2)} ({pctchange2}% change)."
        elif Weapon in list(Shot52.keys()):
            JumpRNG = round(
                self.calcAbilityEffects(AP, Shot52[Weapon][0], Shot52[Weapon][1]), 2
            )
            GroundRNG = round(
                self.calcAbilityEffects(AP, Shot52[Weapon][2], Shot52[Weapon][3]), 2
            )
            return f"Jump shot randomization: {JumpRNG}% of base value. Ground shot randomization: {GroundRNG}% of base value."
        elif Weapon in list(BlasterRangeClash.keys()):
            JumpRNG = round(
                self.calcAbilityEffects(
                    AP, BlasterRangeClash[Weapon][0], BlasterRangeClash[Weapon][1]
                ),
                2,
            )
            return f"Jump shot randomization {JumpRNG}% of base value."
        elif Weapon in list(Rollers.keys()):
            Damage = round(
                self.calcAbilityEffects(AP, Rollers[Weapon][0], Rollers[Weapon][1]), 2
            )
            return f"Roller damage: {Damage}% of base damage."
        elif Weapon == "tent":
            ShieldHealth = self.calcAbilityEffects(
                AP, 700, 1000
            )  # units are tent shield hp
            pctchange = round(self.calcPctChange(700, ShieldHealth), 2)
            return f"Tenta Brella shield health: {round(ShieldHealth,2)} HP ({pctchange}% change)."
        elif Weapon == "luna":
            BlastRadius = round(
                self.calcAbilityEffects(AP, 100, 300), 2
            )  # units are percentage of base value
            Painting = round(self.calcAbilityEffects(AP, 100, 109.375), 2)
            return f"Non-lethal blast radius {BlastRadius}% of base blast radius. Paiting ability: {Painting}% of base paint output"
        elif Weapon == "rapid-blaster" or Weapon == "rapid-pro":
            BlastRadius = round(
                self.calcAbilityEffects(AP, 100, 106.061), 2
            )  # units are percentage of base value
            JumpRNG = round(self.calcAbilityEffects(AP, 100, 50), 2)
            return f"Damage radius: {BlastRadius}% of base damage radius. Jump shot randomization: {JumpRNG}% of base jump shot randomization."
        elif Weapon == "nzap":
            GroundRNG = round(
                self.calcAbilityEffects(AP, 100, 80), 2
            )  # units are percentage of base value
            Painting = round(self.calcAbilityEffects(AP, 100, 113.793), 2)
            return f"Ground shot randomization: {GroundRNG}% of base ground shot randomization. Painting ability: {Painting}% of base painting ability"
        elif Weapon == "slosher":
            DamageRange = self.calcAbilityEffects(AP, 15, 55)  # units unclear
            pctchange = round(self.calcPctChange(15, DamageRange), 2)
            return f"Max damage range: {round(DamageRange,2)} ({pctchange}% change)."
        elif Weapon == "gloogas":
            NormalFireDamage = self.calcAbilityEffects(AP, 36, 43.2)
            TurretModeDamage = self.calcAbilityEffects(AP, 52.5, 63)
            pctchange1 = round(self.calcPctChange(36, NormalFireDamage), 2)
            pctchange2 = round(self.calcPctChange(52.5, TurretModeDamage), 2)
            return f"Damage per shot in regular firing mode: {round(NormalFireDamage,2)} ({pctchange1}% change). Damage per shot in turret mode: {round(TurretModeDamage,2)} ({pctchange2}% change)."
        elif Weapon == "hydra":
            PartialChargeMinDamage = self.calcAbilityEffects(AP, 16, 17.6)
            pctchange1 = round(self.calcPctChange(16, PartialChargeMinDamage), 2)
            PartialChargeMaxDamage = self.calcAbilityEffects(AP, 32, 33.3)
            pctchange2 = round(self.calcPctChange(32, PartialChargeMaxDamage), 2)
            return f"Partial charge minimum damage: {round(PartialChargeMinDamage,2)} ({pctchange1}% change). Partial charge max damage: {round(PartialChargeMaxDamage,2)} ({pctchange2}% change)."
        elif Weapon == "jet":
            ShotSpread = round(self.calcAbilityEffects(AP, 100, 70), 2)
            ShotRangeVelocity = round(self.calcAbilityEffects(AP, 100, 108.46), 2)
            return f"Ground shot randomization: {ShotSpread}% of base value. Range and bullet velocity: {ShotRangeVelocity}% of base value."
        else:
            return "Invalid weapon name entered. Use a.weaponglossary for a list of weapon names."

    def placeholder(self, ctx, AP):
        return "Not programmed yet, check back later."


def setup(bot):
    bot.add_cog(Gearcalcs(bot))
