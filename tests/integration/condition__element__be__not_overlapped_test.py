# MIT License
#
# Copyright (c) 2015-2022 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest

from selene import be
from selene.core import match
from tests.integration.helpers.givenpage import GivenPage


def test_not_overlapped__passed_and_failed(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="not-overlapped" style="position: absolute; top: 0; left: 0;">Click me</button>
            <div id="overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px; display: none;">Overlay</div>
        </div>
        '''
    )

    not_overlapped = browser.element("#not-overlapped")
    overlay = browser.element("#overlay")

    # THEN

    # not overlapped?
    # - not overlapped passes
    not_overlapped.should(be.not_overlapped)
    # not_overlapped.should(match.not_overlapped)

    # Show overlay
    browser.execute_script("document.getElementById('overlay').style.display = 'block'")

    # - now overlapped fails
    try:
        not_overlapped.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)

    # Hide overlay
    browser.execute_script("document.getElementById('overlay').style.display = 'none'")

    # - not overlapped passes again
    not_overlapped.should(be.not_overlapped)


def test_not_overlapped_with_partial_overlap(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="partially-overlapped" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">Click me</button>
            <div id="partial-overlay" style="position: absolute; top: 50px; left: 50px; width: 100px; height: 100px;">Overlay</div>
        </div>
        '''
    )

    partially_overlapped = browser.element("#partially-overlapped")

    # partially overlapped should fail
    try:
        partially_overlapped.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)


def test_not_overlapped_with_no_overlap(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="partially-overlapped" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">Click me</button>
            <div id="partial-overlay" style="position: absolute; top: 150px; left: 150px; width: 50px; height: 50px;">Overlay</div>
        </div>
        '''
    )

    partially_overlapped = browser.element("#partially-overlapped")

    partially_overlapped.should(be.not_overlapped)


def test_not_overlapped_with_transparent_overlay(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="under-transparent" style="position: absolute; top: 0; left: 0;">Click me</button>
            <div id="transparent-overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px; opacity: 0.5;">Overlay</div>
        </div>
        '''
    )

    under_transparent = browser.element("#under-transparent")

    # under transparent overlay fails
    try:
        under_transparent.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)


def test_not_overlapped_with_z_index(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="higher-z-index" style="position: absolute; top: 0; left: 0; z-index: 2;">Click me</button>
            <div id="lower-z-index" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px; z-index: 1;">Overlay</div>
        </div>
        '''
    )

    higher_z_index = browser.element("#higher-z-index")

    # higher z-index passes
    higher_z_index.should(be.not_overlapped)


def test_not_overlapped_with_nested_elements(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <div id="parent" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">
                <button id="child" style="position: relative; width: 50px; height: 50px;">Click me</button>
            </div>
            <div id="overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">Overlay</div>
        </div>
        '''
    )

    child = browser.element("#child")
    parent = browser.element("#parent")

    # Child element should be considered overlapped if parent is overlapped
    try:
        child.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)


def test_not_overlapped_with_dynamic_content(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="target" style="position: absolute; top: 0; left: 0;">Click me</button>
            <div id="overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px; display: none;">Overlay</div>
        </div>
        '''
    )

    target = browser.element("#target")
    overlay = browser.element("#overlay")

    # Initially not overlapped
    target.should(be.not_overlapped)

    # Show overlay with animation
    browser.execute_script(
        """
        var overlay = document.getElementById('overlay');
        overlay.style.display = 'block';
        overlay.style.transition = 'opacity 0.5s';
        overlay.style.opacity = '1';
    """
    )

    # Should detect overlap even during animation
    try:
        target.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)


def test_not_overlapped_with_iframe(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <iframe id="frame" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;" srcdoc="
                <div style='position: absolute; top: 0; left: 0; width: 50px; height: 50px;'>Content</div>
            "></iframe>
            <div id="overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">Overlay</div>
        </div>
        '''
    )

    # Check the iframe element from parent context
    iframe = browser.element("#frame")
    overlay = browser.element("#overlay")

    # The iframe itself should be considered overlapped by the overlay
    try:
        iframe.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)

    # Now check the content inside iframe
    browser.switch_to.frame("frame")
    iframe_content = browser.element("div")

    # The content inside iframe should be considered not overlapped
    iframe_content.should(be.not_overlapped)

    # Switch back to parent context
    browser.switch_to.default_content()

    # Add an overlay inside the iframe
    browser.execute_script(
        """
        var frame = document.getElementById('frame');
        var frameDoc = frame.contentDocument || frame.contentWindow.document;
        var overlay = frameDoc.createElement('div');
        overlay.style.position = 'absolute';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '50px';
        overlay.style.height = '50px';
        overlay.style.backgroundColor = 'red';
        frameDoc.body.appendChild(overlay);
    """
    )

    # Switch back to iframe and check content again
    browser.switch_to.frame("frame")

    # Now the content should be considered overlapped by the iframe overlay
    try:
        iframe_content.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)

    # Switch back to parent context
    browser.switch_to.default_content()


def test_not_overlapped_with_negative_z_index(session_browser):
    browser = session_browser.with_(timeout=0.1)
    GivenPage(session_browser.driver).opened_with_body(
        '''
        <div id="container" style="position: relative; width: 200px; height: 200px;">
            <button id="target" style="position: absolute; top: 0; left: 0; z-index: -1;">Click me</button>
            <div id="overlay" style="position: absolute; top: 0; left: 0; width: 100px; height: 100px;">Overlay</div>
        </div>
        '''
    )

    target = browser.element("#target")

    # Element with negative z-index should be considered overlapped
    try:
        target.should(be.not_overlapped)
        pytest.fail('expect failure')
    except AssertionError as error:
        assert "ConditionMismatch" in str(error)
        assert "is overlapped by" in str(error)
        assert "condition not matched" in str(error)
