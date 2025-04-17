import pytest
from selene import browser, have, be
from tests import resources


@pytest.fixture(scope='function')
def setup_browser():
    """Setup and teardown browser for each test.

    Sets a short timeout and ensures browser is quit after each test.
    """
    # Setup
    browser.config.timeout = 0.5
    yield
    # Teardown
    browser.quit()


def add_todos(count=50):
    """Helper function to add todo items to webpage.

    Args:
        count (int): Number of todo items to add. Defaults to 50.
    """
    for i in range(count):
        browser.element('#new-todo').type(f'todo item {i}').press_enter()


def test_logging_outer_html_with_medium_limit(setup_browser):
    """Test logging of outer HTML with a medium limit of 10 elements.

    Verifies that when logging is enabled and limit is set to 10,
    only 10 elements are shown in the error message with a summary
    of remaining elements.
    """
    browser.config.log_outer_html_on_failure = True
    browser.config.logging_actual_webelements_count_limit = 10
    browser.open(resources.TODOMVC_URL)

    # Add many todo items to ensure we have enough elements
    add_todos(25)

    message = None
    try:
        # Try to find elements with a non-existent attribute
        browser.all('.todo-list li').element_by(have.attribute('nonexistent')).should(
            be.visible
        )
    except Exception as e:
        message = str(e)

    # Verify the message format
    assert message is not None
    assert 'Actual webelements collection' in message
    assert message.count('<li') == 10  # Should show only 10 items

    total_elements = len(browser.all('.todo-list li'))
    assert f'... and {total_elements - 10} more' in message
    assert f'Total number of webelements: {total_elements}' in message


def test_logging_outer_html_with_small_limit(setup_browser):
    """Test logging of outer HTML with a small limit of 3 elements.

    Verifies that when logging is enabled and limit is set to 3,
    only 3 elements are shown in the error message with a summary
    of remaining elements.
    """
    browser.config.log_outer_html_on_failure = True
    browser.config.logging_actual_webelements_count_limit = 3
    browser.open(resources.TODOMVC_URL)

    # Add many todo items
    add_todos(10)

    message = None
    try:
        browser.all('.todo-list li').element_by(have.attribute('nonexistent')).should(
            be.visible
        )
    except Exception as e:
        message = str(e)

    # Verify the message format
    assert message is not None
    assert 'Actual webelements collection' in message
    assert message.count('<li') == 3

    total_elements = len(browser.all('.todo-list li'))
    assert f'... and {total_elements - 3} more' in message
    assert f'Total number of webelements: {total_elements}' in message


def test_logging_outer_html_with_high_limit(setup_browser):
    """Test logging of outer HTML with a high limit of 1000 elements.

    Verifies that when logging is enabled and limit is set to 1000,
    all elements are shown in the error message since the limit is
    higher than the number of elements.
    """
    browser.config.log_outer_html_on_failure = True
    browser.config.logging_actual_webelements_count_limit = 1000
    browser.open(resources.TODOMVC_URL)

    # Add todo items
    add_todos(25)

    message = None
    try:
        browser.all('.todo-list li').element_by(have.attribute('nonexistent')).should(
            be.visible
        )
    except Exception as e:
        message = str(e)

    # Verify the message format
    assert message is not None
    assert 'Actual webelements collection' in message

    total_elements = len(browser.all('.todo-list li'))
    assert f'... and' not in message  # Should show all items since limit is high
    assert f'Total number of webelements: {total_elements}' in message


def test_logging_outer_html_disabled(setup_browser):
    """Test logging behavior when outer HTML logging is disabled.

    Verifies that when logging is disabled, no HTML elements are
    shown in the error message.
    """
    browser.config.log_outer_html_on_failure = False
    browser.open(resources.TODOMVC_URL)

    # Add todo items
    add_todos(10)

    message = None
    try:
        browser.all('.todo-list li').element_by(have.attribute('nonexistent')).should(
            be.visible
        )
    except Exception as e:
        message = str(e)

    assert message is not None
    assert 'Actual webelements collection' not in message
    assert '<li' not in message


def test_logging_outer_html_with_no_limit(setup_browser):
    """Test logging of outer HTML with no limit set.

    Verifies that when logging is enabled and no limit is set,
    all elements are shown in the error message.
    """
    browser.config.log_outer_html_on_failure = True
    browser.config.logging_actual_webelements_count_limit = None
    browser.open(resources.TODOMVC_URL)

    # Add todo items
    add_todos(25)

    message = None
    try:
        browser.all('.todo-list li').element_by(have.attribute('nonexistent')).should(
            be.visible
        )
    except Exception as e:
        message = str(e)

    # Verify the message format
    assert message is not None
    assert 'Actual webelements collection' in message

    total_elements = len(browser.all('.todo-list li'))
    assert f'... and' not in message  # Should show all items since there's no limit
    assert f'Total number of webelements: {total_elements}' in message
