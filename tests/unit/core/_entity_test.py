import pytest


# Dummy Condition class for testing
class Condition:
    def __init__(self, predicate):
        self.predicate = predicate


# Dummy Wait class to support the methods
class Wait:
    def for_(self, condition):
        pass

    def until(self, condition):
        return True


# Class under test
class MyObject:
    def __init__(self):
        self.wait = Wait()

    def should(self, condition: Condition) -> "MyObject":
        if not isinstance(condition, Condition):
            raise ValueError('condition must be an instance of Condition')
        self.wait.for_(condition)
        return self

    def wait_until(self, condition: Condition) -> bool:
        if not isinstance(condition, Condition):
            raise ValueError('condition must be an instance of Condition')
        return self.wait.until(condition)

    def matching(self, condition: Condition) -> bool:
        if not isinstance(condition, Condition):
            raise ValueError('condition must be an instance of Condition')
        return condition.predicate(self)


# --- Tests ---
@pytest.fixture
def obj():
    return MyObject()


def test_should_with_invalid_type_raises(obj):
    with pytest.raises(ValueError, match="condition must be an instance of Condition"):
        obj.should("not a condition")


def test_wait_until_with_invalid_type_raises(obj):
    with pytest.raises(ValueError, match="condition must be an instance of Condition"):
        obj.wait_until(123)


def test_matching_with_invalid_type_raises(obj):
    with pytest.raises(ValueError, match="condition must be an instance of Condition"):
        obj.matching(None)


def test_should_with_valid_condition(obj):
    cond = Condition(lambda x: True)
    result = obj.should(cond)
    assert result is obj


def test_wait_until_with_valid_condition(obj):
    cond = Condition(lambda x: True)
    result = obj.wait_until(cond)
    assert result is True


def test_matching_with_valid_condition(obj):
    cond = Condition(lambda x: True)
    result = obj.matching(cond)
    assert result is True
