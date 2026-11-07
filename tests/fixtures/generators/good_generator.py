# TEST FIXTURE for the I2 static check: reads specs only through ctx.spec().
def generate(p, ctx):
    servo = ctx.part(p.servo)
    body_l = ctx.spec(servo, "body_l_mm")  # raises MissingSpec if null
    return {"base": body_l}
