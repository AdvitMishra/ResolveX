def check_exam_submission(minutes_left: int) -> str:
    # BUG: Auto-submits when 10 minutes remain instead of 0
    if minutes_left <= 0:
        return "AUTO_SUBMIT"
    return "IN_PROGRESS"
