import pytest
import pytest_html


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")
    cells.insert(3, "<th>Image</th>")


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.description}</td>")
    cells.insert(3, f"<td>{report.image}</td>")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    raw_image = getattr(report, "user_properties", None)
    report.image = raw_image[0][1] if raw_image else None
    report.description = str(item._obj.__doc__.strip())
    # extras = getattr(report, "extras", [])
    # extras.append(pytest_html.extras.
