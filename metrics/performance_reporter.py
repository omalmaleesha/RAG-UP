from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


class PerformanceReporter:

    REPORT_DIR = Path("metrics")
    REPORT_FILE = REPORT_DIR / "test_metrics.txt"

    @staticmethod
    def create_report_file():
        """
        Create the metrics directory and report file if they don't exist.
        """

        PerformanceReporter.REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        if not PerformanceReporter.REPORT_FILE.exists():
            PerformanceReporter.REPORT_FILE.touch()

    @staticmethod
    def write(result):
        """
        Write one complete performance report to test_metrics.txt.
        """

        PerformanceReporter.create_report_file()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        metrics = result.get("metrics", {})

        lines = []

        lines.append("")
        lines.append("=" * 70)
        lines.append("RAG AI AGENT PERFORMANCE REPORT")
        lines.append("=" * 70)

        lines.append(
            f"Timestamp       : {timestamp}"
        )

        lines.append(
            f"User Query      : {result.get('user_query', 'N/A')}"
        )

        lines.append("-" * 70)

        # Cache information
        lines.append("CACHE")
        lines.append("-" * 70)

        lines.append(
            f"Cache Hit       : {result.get('cache_hit', False)}"
        )

        lines.append(
            f"Cached Answer   : "
            f"{'Yes' if result.get('cached_answer') else 'No'}"
        )

        lines.append("-" * 70)

        # Tool information
        lines.append("TOOL / ROUTING")
        lines.append("-" * 70)

        lines.append(
            f"Selected Tool   : "
            f"{result.get('selected_tool') or 'None'}"
        )

        lines.append(
            f"LLM Calls       : "
            f"{result.get('llm_calls', 0)}"
        )

        lines.append(
            f"Enough Info     : "
            f"{result.get('enough_information', False)}"
        )

        lines.append("-" * 70)

        # Node performance
        lines.append("NODE EXECUTION TIMES")
        lines.append("-" * 70)

        if metrics:

            lines.append(
                f"{'Node':<30}{'Time (s)':>15}"
            )

            lines.append("-" * 45)

            for node, execution_time in metrics.items():

                lines.append(
                    f"{node:<30}"
                    f"{execution_time:>15.3f}"
                )

        else:

            lines.append("No node metrics recorded.")

        lines.append("-" * 70)

        # Overall performance
        lines.append("OVERALL PERFORMANCE")
        lines.append("-" * 70)

        lines.append(
            f"Total Time     : "
            f"{result.get('total_time', 0):.3f}s"
        )

        lines.append(
            f"Reflection     : "
            f"{result.get('reflection_passed', False)}"
        )

        lines.append(
            f"Retrieved Docs : "
            f"{len(result.get('retrieved_docs', []))}"
        )

        lines.append("-" * 70)

        # Final answer information
        final_answer = result.get("final_answer")

        lines.append("RESPONSE")
        lines.append("-" * 70)

        if final_answer:
            lines.append(final_answer)
        else:
            lines.append("No final answer generated.")

        lines.append("=" * 70)
        lines.append("END OF REPORT")
        lines.append("=" * 70)
        lines.append("")

        report_text = "\n".join(lines)

        # Append instead of overwrite
        with PerformanceReporter.REPORT_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(report_text)

    @staticmethod
    def print(result):

        print("\n")
        print("=" * 50)
        print("PERFORMANCE")
        print("=" * 50)

        print(
            f"Cache Hit : {result.get('cache_hit', False)}"
        )

        print(
            f"Tool      : "
            f"{result.get('selected_tool') or 'None'}"
        )

        print()

        for node, execution_time in result.get(
            "metrics",
            {}
        ).items():

            print(
                f"{node:<25} "
                f"{execution_time:.3f}s"
            )

        print("-" * 50)

        print(
            f"Total     : "
            f"{result.get('total_time', 0):.3f}s"
        )

        print(
            f"LLM Calls : "
            f"{result.get('llm_calls', 0)}"
        )

        print("=" * 50)
        
        
    @staticmethod
    def txt_to_pdf():
        """
        Convert the existing test_metrics.txt file
        into a professionally formatted PDF.
        """

    
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            KeepTogether
        )
        from reportlab.lib.units import mm
        from xml.sax.saxutils import escape

        # --------------------------------------------------
        # Paths
        # --------------------------------------------------

        txt_file = PerformanceReporter.REPORT_FILE

        pdf_dir = PerformanceReporter.REPORT_DIR / "reports"

        pdf_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf_file = pdf_dir / "rag_performance_report.pdf"

        # --------------------------------------------------
        # Check TXT file
        # --------------------------------------------------

        if not txt_file.exists():
            print(
                f"Report file not found: {txt_file}"
            )
            return None

        # --------------------------------------------------
        # Read existing report
        # --------------------------------------------------

        with txt_file.open(
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        if not content.strip():
            print("Report file is empty.")
            return None

        # --------------------------------------------------
        # PDF document
        # --------------------------------------------------

        document = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title="RAG AI Agent Performance Report"
        )

        # --------------------------------------------------
        # Styles
        # --------------------------------------------------

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=5
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=18
        )

        section_style = ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=12,
            spaceAfter=7
        )

        normal_style = ParagraphStyle(
            "NormalReport",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13
        )

        response_style = ParagraphStyle(
            "Response",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14
        )

        # --------------------------------------------------
        # Story
        # --------------------------------------------------

        story = []

        # Header
        story.append(
            Paragraph(
                "RAG AI AGENT",
                title_style
            )
        )

        story.append(
            Paragraph(
                "Performance Evaluation Report",
                subtitle_style
            )
        )

        # --------------------------------------------------
        # Split multiple reports
        # --------------------------------------------------

        reports = content.split(
            "RAG AI AGENT PERFORMANCE REPORT"
        )

        report_number = 0

        for report in reports:

            if not report.strip():
                continue

            report_number += 1

            # Start a new report section
            if report_number > 1:
                story.append(
                    Spacer(1, 12)
                )

            # --------------------------------------------------
            # Parse lines
            # --------------------------------------------------

            lines = [
                line.strip()
                for line in report.splitlines()
                if line.strip()
            ]

            current_section = None
            table_rows = []
            response_lines = []

            sections = {
                "CACHE",
                "TOOL / ROUTING",
                "NODE EXECUTION TIMES",
                "OVERALL PERFORMANCE",
                "RESPONSE"
            }

            for line in lines:

                # Ignore decorative separators
                if set(line) <= {"=", "-"}:
                    continue

                # Detect sections
                if line in sections:

                    # Flush previous table
                    if table_rows:
                        story.append(
                            Table(
                                table_rows,
                                colWidths=[
                                    75 * mm,
                                    90 * mm
                                ]
                            )
                        )

                        table_rows = []

                    current_section = line

                    story.append(
                        Paragraph(
                            line.title(),
                            section_style
                        )
                    )

                    continue

                # --------------------------------------------------
                # Response section
                # --------------------------------------------------

                if current_section == "RESPONSE":

                    if line != "END OF REPORT":
                        response_lines.append(line)

                    continue

                # --------------------------------------------------
                # Node execution table
                # --------------------------------------------------

                if current_section == "NODE EXECUTION TIMES":

                    if line.startswith("Node"):
                        table_rows.append(
                            [
                                Paragraph(
                                    "<b>Node</b>",
                                    normal_style
                                ),
                                Paragraph(
                                    "<b>Time</b>",
                                    normal_style
                                )
                            ]
                        )
                        continue

                    # Example:
                    # planner                       0.235s

                    parts = line.rsplit(
                        " ",
                        1
                    )

                    if len(parts) == 2:

                        node = parts[0]
                        value = parts[1]

                        table_rows.append(
                            [
                                Paragraph(
                                    escape(node),
                                    normal_style
                                ),
                                Paragraph(
                                    escape(value),
                                    normal_style
                                )
                            ]
                        )

                    continue

                # --------------------------------------------------
                # Normal key/value sections
                # --------------------------------------------------

                if ":" in line:

                    key, value = line.split(
                        ":",
                        1
                    )

                    table_rows.append(
                        [
                            Paragraph(
                                f"<b>{escape(key.strip())}</b>",
                                normal_style
                            ),
                            Paragraph(
                                escape(value.strip()),
                                normal_style
                            )
                        ]
                    )

            # --------------------------------------------------
            # Flush remaining table
            # --------------------------------------------------

            if table_rows:

                table = Table(
                    table_rows,
                    colWidths=[
                        75 * mm,
                        90 * mm
                    ],
                    repeatRows=1
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.HexColor(
                                    "#E9EEF5"
                                )
                            ),
                            (
                                "BOX",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.grey
                            ),
                            (
                                "INNERGRID",
                                (0, 0),
                                (-1, -1),
                                0.25,
                                colors.lightgrey
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "MIDDLE"
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                8
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                8
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            )
                        ]
                    )
                )

                story.append(table)

            # --------------------------------------------------
            # Response
            # --------------------------------------------------

            if response_lines:

                response_text = "<br/>".join(
                    escape(line)
                    for line in response_lines
                )

                response_table = Table(
                    [
                        [
                            Paragraph(
                                response_text,
                                response_style
                            )
                        ]
                    ],
                    colWidths=[
                        165 * mm
                    ]
                )

                response_table.setStyle(
                    TableStyle(
                        [
                            (
                                "BOX",
                                (0, 0),
                                (-1, -1),
                                0.7,
                                colors.grey
                            ),
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, -1),
                                colors.HexColor(
                                    "#F7F9FC"
                                )
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                10
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                10
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                10
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                10
                            )
                        ]
                    )
                )

                story.append(response_table)

        # --------------------------------------------------
        # Build PDF
        # --------------------------------------------------

        document.build(story)

        print(
            f"\nPDF report created: {pdf_file}"
        )

        return pdf_file