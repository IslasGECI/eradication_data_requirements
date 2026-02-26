# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Fixed

### Changed

### Removed

## [8.0.1] - 2026-02-25

### Fixed
- Stream the response of `/write_effort_and_captures_with_probability` entrypoint.

## [8.0.0] - 2026-02-25

### Fixed
- Add `async` to `/write_effort_and_captures_with_probability` in order to wait for longer proccesed time.

### Changed
- The following entrypoints changed from `GET` to `POST`:
  - `/write_population_status_from_mixed_methods`
  - `/filter_by_method`
  - `/write_bootstrap_progress_intervals_json`
  - `/write_aerial_monitoring`

## [7.1.0] - 2026-02-12
### Added
- The entrypoint `/write_effort_and_captures_with_probability` now accepts a temporal resolution parameter. If not provided, the resolution defaults to the window length.

### Changed
- Upgrade `geci-plots==0.9.*` dependency.

## [7.0.1] - 2025-12-09
### Fixed
- The function `select_month_by_window_length()` now give us unique indices. Now the functions `paste_status_by_window()` and `calculate_resampled_by_window()` dataframes with the same length.

## [7.0.0] - 2025-09-03
### Added
- The entrypoint `/plot_cumulative_series_cpue_by_season`. We calculate the yearly CPUE and cumulative CPUE for effort and capture datasets.
- The entrypoint `/plot_comparative_yearly_cpue`. With this entrypoint we can combine the yearly CPUE for effort and capture datasets.

### Changed
- The entrypoint `/plot_cumulative_series_cpue_by_flight` no longer reads or writes to disk; it now receives a POST request with a CSV file and returns a JSON response.


## [6.0.1] - 2025-08-04
### Fixed
- The entrypoint `/write_effort_and_captures_with_probability` now correctly handles the `window_length` argument, ensuring it only processes the specified months of interest. See function `get_ramsey_series_window()`.

## [6.0.0] - 2025-08-04
### Changed
- The entrypoint `/plot_comparative_catch_curves` no longer reads or writes to disk; it now receives a POST request with a CSV file and returns a JSON response.

## [5.0.0] - 2025-07-31
### Changed
- The entrypoints `/plot_cpue_vs_cum_captures` and `/plot_custom_cpue_vs_cum_captures` no longer reads or writes to disk; it now receives a POST request with a CSV file and returns a JSON response.

## [4.0.1] - 2025-07-30
### Fixed
- The function `calculate_resampled_probability_by_window()` now uses the `window_length` argument to calculate only the months of interest, instead of the entire year.

## [4.0.0] - 2025-07-15
### Changed
- The entrypoints `/write_effort_and_captures_with_probability` and `/write_probability_figure` no longer reads or writes to disk; it now receives a POST request with a CSV file and returns a JSON response.

### Removed
- CLI commands `write_progress_probability_figure`, `write_effort_and_captures_with_probability`.

## [3.0.0] - 2025-07-11
### Changed
- The entrypoint `/write_population_status` no longer reads or writes to disk; it now receives a POST request with a CSV file and returns a JSON response.

## [2.1.1] - 2025-01-21

### Changed
- The function `add_probs_to_effort_capture_data` used by cli command and entrypoint `write_effort_and_captures_with_probability` now fill missing months in the data.
- The function `plot_progress_probability()` now plots all rows given.

## [2.1.0] - 2025-01-15

### Added
- New entrypoint `/write_population_status_from_mixed_methods` to mix the distributions from to hunting methods.

### Changed
- The entrypoint `/write_population_status` now saves the n0 distribution.

## [2.0.0] - 2024-12-16

### Added
- The class `ProgressBootstrapper` to get slopes boostrap distribution json

### Fixed

### Changed
- Change implementation of function `write_effort_and_captures_with_probability`. Now uses `calculate_resampled_probability_by_window()` that resample, sort and then acumulates to get the progress probability. Also, the resolution is fixed to give the last month of the year. Please, refers to issue [#556](https://github.com/IslasGECI/kanban/issues/556)

### Removed

## [1.7.2] - 2024-10-02
### Changed
- The entrypoint `/write_population_status` now calculates the CPUE from Esfuerzo and Capturas columns

## [1.7.1] - 2024-09-24
### Changed
- Add the progress probability to entrypoint `/write_population_status`

## [1.7.0] - 2024-09-23

### Add
- Entrypoint `/write_aerial_monitoring` to calculate total population of feral goat confidence interval from aerial monitoring.

## [1.6.0] - 2024-09-17

### Add
- Entrypoint `/filter_by_method` to filter by removals technique.

### Changed
- Entrypoint `/write_population_status` discards initial population lower than total captures.


## [1.5.0] - 2024-09-13

### Add
- Entrypoint `/write_population_status` for population status after eradication effort.


## [1.4.0] - 2024-07-26

### Add
- Entrypoint `/plot_custom_cpue_vs_cum_captures` for plot cpue vs cumulative captures (Ramsey's plot) with customize json

## [1.3.0] - 2024-07-16

### Add
- Entrypoint for cpue feral goat eradication
- Cli commands `plot_cumulative_series_cpue_by_flight()` and `plot_cumulative_series_cpue_by_season()`

## [1.2.0] - 2023-10-11

### Add
- Entrypoint for comparative plot of catch curves (Ramsey's plot)

## [1.1.0] - 2023-10-10

### Add
- Entrypoint for plot cpue vs cumulative captures (Ramsey's plot)

## [1.0.1] - 2023-09-22

### Changed
- The resampling occurs over the `Cumulative_captures`

## [1.0.0] - 2023-09-21

### Added
- Add window length argument to `add_probs_to_effort_capture_data()`, `write_effort_and_captures_with_probability()` and entrypoint `/write_effort_and_captures_with_probability`

### Removed
- Deleted function `calculate_resample_six_month_slope()`

## [0.3.0] - 2023-09-20

### Added

- New argument `bootstrapping_number` in function `write_effort_and_captures_with_probability()` and his dependencies.

### Fixed

- New resample method in `resample_fit_ramsey_plot()` using moving block bootstrapping with blocks of length 2.

### Removed

- Function `remove_non_consecutive_captures()`. Resample method now validate samples to fit using `validate_samples_to_fit()`.

## [0.2.0] - 2023-09-15

### Added

- Move functions `write_progress_probability_figure`, `write_effort_and_captures_with_probability`, `write_effort_and_captures_with_slopes` from `gatos` repository

### Fixed

### Changed
- Change hash for `data_requirements_plot`

## [0.1.1] - 2023-07-25

### Added

- CHANGELOG.


### Changed
- Change hash for `data_requirements_plot` because matplotlib upgrade version 3.7.2.

[unreleased]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.8.0...HEAD
[8.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.3.0...v8.0.0
[7.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v6.0.0...v7.0.0
[6.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v5.0.0...v6.0.0
[5.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v4.0.0...v5.0.0
[4.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v3.0.0...v4.0.0
[3.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.3.0...v0.2.0
[0.2.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.2.0...v0.1.1
[0.1.1]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.1.0...v0.1.1
