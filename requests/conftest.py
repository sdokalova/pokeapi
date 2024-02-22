import pytest


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(3, "<th>Image</th>")
    cells.insert(4, "<th>Assertions</th>")


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.description}</td>")
    cells.insert(3, f"<td>{report.image}</td>")
    cells.insert(4, f"<td>{report.assertions}</td>")


asserts = dict()

@pytest.mark.optionalhook
def pytest_assertion_pass(item, lineno, orig, expl):
    asserts


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    raw_image = getattr(report, "user_properties", None)
    report.image = raw_image[0][1] if raw_image else None
    report.description = str(item._obj.__doc__.strip())
    report.assertions = asserts
