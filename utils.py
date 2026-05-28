import streamlit as st
import streamlit.components.v1 as components


_CSS = """
p, li,
label, label *,
textarea, input,
[data-testid="stMarkdownContainer"] *,
[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span,
[data-testid="stWidgetLabel"] *,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stCaptionContainer"] *,
[data-testid="stExpander"] summary *,
.stButton > button,
.stButton > button * {
    font-size: 20px !important;
    line-height: 1.8 !important;
}
"""

# Escape backticks and backslashes for use inside a JS template literal
_JS_CSS = _CSS.replace("\\", "\\\\").replace("`", "\\`")


def apply_user_css(user_type: str) -> None:
    if user_type != "고령층":
        return

    # Layer 1: st.markdown CSS (within-body injection)
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)

    # Layer 2: JS injects <style> at end of <head>.
    # Disconnects observer before DOM mutation to prevent infinite loop.
    components.html(
        f"""<script>
(function() {{
  var css = `{_JS_CSS}`;
  var obs = new MutationObserver(function() {{ inject(); }});

  function inject() {{
    obs.disconnect();
    var doc = window.parent.document;
    var old = doc.getElementById('jb-user-css');
    if (old) old.remove();
    var s = doc.createElement('style');
    s.id = 'jb-user-css';
    s.textContent = css;
    doc.head.appendChild(s);
    obs.observe(doc.head, {{ childList: true }});
  }}

  inject();
}})();
</script>""",
        height=1,
    )
