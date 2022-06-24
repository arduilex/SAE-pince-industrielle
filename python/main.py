#!/usr/bin/python3
import asyncio, pifacecad
import RPi.GPIO as GPIO
from appli import Application

cad = pifacecad.PiFaceCAD()
app = Application(cad)

async def update_buttons():
    pin_buttons = [0, 1, 2, 3, 4]
    buttons = [0]*len(pin_buttons)
    old_buttons = buttons[:]
    while 1:
        buttons = [cad.switches[pin].value for pin in pin_buttons]
        if buttons != old_buttons and sum(buttons):
            if buttons[4]:
                app.action_enter()
            elif buttons[3]:
                app.action_cursor(sens=1)
            elif buttons[2]:
                app.action_cursor(sens=-1)
            else:
                app.action_button(buttons.index(1))
            await asyncio.sleep(0.1)
        old_buttons = buttons[:]
        await asyncio.sleep(0.01)

async def update_mesure():
    while 1:
        if app.parameter["mod"]=="auto":
            app.get_mesure()
            app.update_led()
            app.update_optoc()
        await asyncio.sleep(app.delay)

async def update_lcd():
    while 1:
        if app.parameter["mod"]=="auto" and app.id_menu=="home": 
            app.update_mesure()
        await asyncio.sleep(0.5)

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(update_buttons(), update_mesure(), update_lcd())

asyncio.run(main())