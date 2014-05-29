def heading_error(initial, final):
    assert initial <= 360
    assert initial >= 0
    assert final <= 360
    assert final >= 0

    diff = final - initial
    absDiff = abs(diff)

    if absDiff <= 180:
        if absDiff == 180:
            return absDiff
        else:
            return diff;
    elif final > initial:
        return absDiff - 360
    else:
        return 360 - absDiff
