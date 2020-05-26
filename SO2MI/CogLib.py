from SO2MI.config import CONFIG

def chk_channel(ctx):
    return ctx.message.channel.id == int(CONFIG["discord"]["channel"])
