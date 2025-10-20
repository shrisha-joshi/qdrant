pub mod condition;
pub mod field_condition;
pub mod geo;
pub mod r#match;
pub mod min_should;
pub mod nested;
pub mod range;
pub mod value_count;

use condition::PyCondition;
use derive_more::Into;
use pyo3::{PyErr, pyclass, pymethods};
use segment::types::{Condition, Filter, MinShould};

use crate::types::filter::min_should::PyMinShould;

#[pyclass(name = "Filter")]
#[derive(Clone, Debug, Into)]
#[repr(transparent)]
pub struct PyFilter(pub Filter);

#[pymethods]
impl PyFilter {
    #[new]
    #[pyo3(signature = (must=None, should=None, must_not=None, min_should=None))]
    pub fn new(
        must: Option<Vec<PyCondition>>,
        should: Option<Vec<PyCondition>>,
        must_not: Option<Vec<PyCondition>>,
        min_should: Option<PyMinShould>,
    ) -> Result<Self, PyErr> {
        let must: Option<Vec<_>> = must.map(|must| must.into_iter().map(Condition::from).collect());
        let should: Option<Vec<_>> =
            should.map(|should| should.into_iter().map(Condition::from).collect());
        let must_not: Option<Vec<_>> =
            must_not.map(|must_not| must_not.into_iter().map(Condition::from).collect());

        let min_should: Option<MinShould> = min_should.map(|min_should| min_should.0);

        Ok(Self(Filter {
            should,
            min_should,
            must,
            must_not,
        }))
    }
}
