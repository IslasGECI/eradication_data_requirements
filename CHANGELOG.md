# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- The class `ProgressBootstrapper` to get slopes boostrap distribution json

### Fixed

### Changed

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

[unreleased]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.3.0...v0.2.0
[0.2.0]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.2.0...v0.1.1
[0.1.1]: https://github.com/IslasGECI/eradication_data_requirements/compare/v0.1.0...v0.1.1
