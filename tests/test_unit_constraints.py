import pandas as pd
from pandas._testing import assert_frame_equal
from nempy import unit_constraints


def test_create_constraints():
    unit_limit = pd.DataFrame({
        'unit': ['A', 'B'],
        'upper': [16.0, 23.0]
    })
    next_constraint_id = 4
    rhs_col = 'upper'
    direction = '<='
    output = unit_constraints.create_constraints(unit_limit, next_constraint_id, rhs_col, direction)
    expected = pd.DataFrame({
        'constraint_id': [4, 5],
        'unit': ['A', 'B'],
        'rhs': [16.0, 23.0],
        'coefficient': [1.0, 1.0],
        'type': ['<=', '<='],
        'service': ['energy', 'energy']
    })
    assert_frame_equal(output, expected)


def test_one_unit_create_constraints():
    unit_limit = pd.DataFrame({
        'unit': ['A'],
        'upper': [16.0]
    })
    next_constraint_id = 4
    rhs_col = 'upper'
    direction = '<='
    output = unit_constraints.create_constraints(unit_limit, next_constraint_id, rhs_col, direction)
    expected = pd.DataFrame({
        'constraint_id': [4],
        'unit': ['A'],
        'rhs': [16.0],
        'coefficient': [1.0],
        'type': ['<='],
        'service': ['energy'],
    })
    assert_frame_equal(output, expected)


def test_ramp_down():
    unit_limit = pd.DataFrame({
        'unit': ['A', 'B'],
        'initial_output': [16.0, 23.0],
        'ramp_down_rate': [12.0, 36.0]
    })
    next_constraint_id = 4
    dispatch_interval = 5
    output_rhs = unit_constraints.ramp_down(unit_limit, next_constraint_id, dispatch_interval)
    expected_rhs = pd.DataFrame({
        'unit': ['A', 'B'],
        'constraint_id': [4, 5],
        'type': ['>=', '>='],
        'rhs': [15.0, 20.0],
        'coefficient': [1.0, 1.0],
        'service': ['energy', 'energy']
    })
    assert_frame_equal(output_rhs.reset_index(drop=True), expected_rhs)


def test_ramp_up():
    unit_limit = pd.DataFrame({
        'unit': ['A', 'B'],
        'initial_output': [16, 23],
        'ramp_up_rate': [12, 36]
    })
    next_constraint_id = 4
    dispatch_interval = 5
    output_rhs = unit_constraints.ramp_up(unit_limit, next_constraint_id, dispatch_interval)
    expected_rhs = pd.DataFrame({
        'unit': ['A', 'B'],
        'constraint_id': [4, 5],
        'type': ['<=', '<='],
        'rhs': [17.0, 26.0],
        'coefficient': [1.0, 1.0],
        'service': ['energy', 'energy']
    })
    assert_frame_equal(output_rhs.reset_index(drop=True), expected_rhs)


def test_capacity():
    unit_limit = pd.DataFrame({
        'unit': ['A', 'B'],
        'capacity': [16.0, 23.0]
    })
    next_constraint_id = 4
    output_rhs = unit_constraints.capacity(unit_limit, next_constraint_id)
    expected_rhs = pd.DataFrame({
        'unit': ['A', 'B'],
        'constraint_id': [4, 5],
        'type': ['<=', '<='],
        'rhs': [16.0, 23.0],
        'coefficient': [1.0, 1.0],
        'service': ['energy', 'energy']
    })
    assert_frame_equal(output_rhs.reset_index(drop=True), expected_rhs)
