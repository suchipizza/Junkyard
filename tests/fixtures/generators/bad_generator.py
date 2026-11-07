# TEST FIXTURE for the I2 static check: reads a spec directly (forbidden).
def generate(p, ctx):
    servo = ctx.part(p.servo)
    body_l = servo.specs["body_l_mm"].value or 23  # silent guess when null
    return {"base": body_l}
