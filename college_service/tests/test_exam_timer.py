from college_service.exam_timer import check_exam_submission

def test_exam_continues_at_10_minutes():
    assert check_exam_submission(10) == "IN_PROGRESS"

def test_exam_submits_at_zero():
    assert check_exam_submission(0) == "AUTO_SUBMIT"
