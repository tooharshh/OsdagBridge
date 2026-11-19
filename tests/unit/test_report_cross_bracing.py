from osdagbridge.core.reports import report_generator as report
from osdagbridge.core.reports.chap5 import ch5_design_checks


def test_cross_bracing_uses_stored_force_and_verdict():
    pair = "G1-G2"
    outputs = {
        "crossbracing_forces_dict": {"pairs": {pair: {
            "diag_tension_kN": 9, "diag_compression_kN": 5.25,
            "diag_compression_gov_lc": "Compression case",
        }}},
        "crossbracing_design_results": {pair: {
            "diagonal": {
                "tension": {"Member.efficiency": 0.2, "Design.Status": True},
                "compression": {
                    "Member.efficiency": 0.48, "Member.tension_capacity": 18.4,
                    "Design.Status": False,
                },
            },
            "chord": {"tension": {"Member.efficiency": 1.0, "Design.Status": False}},
        }},
    }
    chapter = ch5_design_checks([], report.ReportDataBridge(outputs, {}, None))
    assert "Diagonal (tension)" in chapter and "Diagonal (compression)" in chapter
    assert "Chord (compression)" not in chapter
    compression = next(line for line in chapter.splitlines()
                       if line.startswith("Cross Bracing --- Compression"))
    assert "5.25 kN" in compression and "8.83 kN" not in compression
    assert "FAIL" in compression
    tension = next(line for line in chapter.splitlines()
                   if line.startswith("Cross Bracing --- Tension"))
    assert "1.00" in tension and "FAIL" in tension and "kN" not in tension
