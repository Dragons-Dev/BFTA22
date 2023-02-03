from datetime import date, time

import discord
from discord.ext import commands, tasks

import config
from utils import db


class HausaufgabenCog(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client
        self.reminder.start()

    @tasks.loop(minutes = 1)
    async def reminder(self):
        await self.client.wait_until_ready()
        fetched_entries = await db.get_hausaufgaben()
        em = discord.Embed(title = "Bevorstehende Hausaufgaben")
        print(fetched_entries)
        channel = self.client.get_channel(1071014318885310524)
        em = discord.Embed(title = "Hausaufgaben")
        if not fetched_entries:
            em.add_field(name = "",
                         value = "KEINE :tada:")
        else:
            n = 0
            for entry in fetched_entries:
                datum = entry[3].split("-")
                datum = f"{datum[2]}.{datum[1]}.{datum[0]}"
                em.add_field(name = f"ID: {entry[0]}",
                             value = f"{entry[1]}: {entry[2]} zum {datum}",
                             inline = False)
                n += 1
                if n >= 24:
                    break
        await channel.send(embed = em)

    @commands.slash_command(name = "hausaufgaben", description = "Füge Hausaufgaben zur Erinnerung hinzu")
    async def hausaufgaben(self,
                           ctx: discord.ApplicationContext,
                           fach: discord.Option(required = True),
                           aufgabe: discord.Option(required = True),
                           wann: discord.Option(required = True,
                                                description = "Bitte halte dich an folgendes format Tag.Monat.Jahr (z.B. 02.02.2023)")
                           ):
        wann = wann.split(".")
        wann = date(year = int(wann[2]), month = int(wann[1]), day = int(wann[0]))
        em = discord.Embed(title = "Die Hausaufgabe wurde registriert!",
                           description = f"Fach: {fach}\nAufgabe: {aufgabe}\nWann: {wann.strftime('%d.%m.%Y')}")
        await ctx.response.send_message(embed = em)
        await db.insert_hausaufgaben(fach = fach,
                                     aufgabe = aufgabe,
                                     wann = wann)


def setup(client: discord.Bot):
    client.add_cog(HausaufgabenCog(client))
