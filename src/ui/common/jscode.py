from st_aggrid import JsCode

INCOMPLETE_CELL_STYLE = JsCode("""
function(params) {
    if (params.value === null || params.value === undefined || params.value === '') {
        return { backgroundColor: '#ffd6d6', border: '1px solid #ff4444' };
    }
    return {};
}
""")

IMPACT_DIFF_CELL_STYLE = JsCode("""
function(params) {
    if (!params.value || params.value === '') return { color: 'gray' };
    const val = parseFloat(params.value);
    if (isNaN(val) || val === 0) return { color: 'gray' };
    return val < 0
        ? { color: '#2d9e2d', fontWeight: 'bold' }
        : { color: '#d9363e', fontWeight: 'bold' };
}
""")

IMPACT_DIFF_TOOLTIP = JsCode("""
function(params) {
    return 'Impact difference if switching to the New Model configuration';
}
""")
