#!/bin/bash
# 运行所有复现的高级图表测试脚本

export PYTHONPATH=../src

echo "==========================================="
echo "   SlanPlot Master Demo Execution Script"
echo "==========================================="

run_demo() {
    echo "Running $1..."
    python "$1"
    if [ $? -eq 0 ]; then
        echo "✅ Success: $1"
    else
        echo "❌ Failed: $1"
    fi
    echo "-------------------------------------------"
}

run_demo "demo_upset.py"
run_demo "demo_joyplot.py"
run_demo "demo_sankey.py"
run_demo "demo_chord.py"
run_demo "demo_stree.py"
run_demo "demo_circ_tree.py"
run_demo "demo_pitree.py"
run_demo "demo_pi_art.py"
run_demo "demo_marginal.py"
run_demo "demo_marginal_errorbar.py"
run_demo "demo_hatched.py"
run_demo "demo_calendar.py"
run_demo "demo_venn.py"
run_demo "demo_sheatmap.py"
run_demo "scientific_viz_1.py"
run_demo "scientific_viz_2.py"

echo "All demos have been executed!"
