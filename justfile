# ==============================================
# Griffin Exam Rendering (Minimal Version)
# ==============================================

TEMPLATE := "{{env_var('HOME')}}/.local/share/griffin_tools/templates/exam_template.tex"

exam md:
    pandoc "{{md}}" \
      --from markdown+yaml_metadata_block \
      --template={{TEMPLATE}} \
      --pdf-engine=pdflatex \
      -o "{{md | replace_regex('\\.md$', '.pdf')}}"

exam-tex md:
    pandoc "{{md}}" \
      --from markdown+yaml_metadata_block \
      --template={{TEMPLATE}} \
      -o "{{md | replace_regex('\\.md$', '.tex')}}"