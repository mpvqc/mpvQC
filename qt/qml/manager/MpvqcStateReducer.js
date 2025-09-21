// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

// .pragma library todo enable

/**
 * @param {string | null | undefined} video
 * @returns {ApplicationState}
 */
function initialState(video) {
    return { kind: "initial", document: null, video: video ?? null, saved: true };
}

/**
 * @param {string | null | undefined} document
 * @param {string | null | undefined} video
 * @param {boolean | undefined} saved
 * @returns {ApplicationState}
 */
function otherState(document, video, saved) {
    return {
        kind: "other",
        document: document ?? null,
        video: video ?? null,
        saved: !!saved,
    };
}

/**
 * @param {ImportChange} change
 * @returns {boolean}
 */
function onlyVideoImported(change) {
    return change.video !== null && (change.documents ?? []).length === 0;
}

/**
 * @param {ImportChange} change
 * @returns {boolean}
 */
function exactlyOneDocumentImported(change) {
    return (change.documents ?? []).length === 1;
}

/**
 * @param {ImportChange} change
 * @returns {string}
 */
function firstImportedDocument(change) {
    return (change.documents ?? [])[0];
}

/**
 * @param {ApplicationState} state
 * @param {Event} event
 * @param {ReducerOptions=} options
 * @returns {ApplicationState}
 */
function reducer(state, event, options) {
    switch (event.type) {
        case "SAVE":
            return otherState(event.document, state.video, true);
        case "CHANGE":
            return otherState(state.document, state.video, false);
        case "RESET":
            return initialState(state.video);
        case "IMPORT":
            return reduceImport(state, event.change);
        default:
            throw new Error(`Unknown event: ${event?.type}`);
    }
}

/**
 * @param {ApplicationState} state
 * @param {ImportChange} change
 * @param {VideoEquals} videoEquals
 * @returns {ApplicationState}
 */
function reduceImport(state, change) {
    switch (state.kind) {
        case "initial":
            return handleImportInInitial(state, change);
        case "other":
            return handleImportInOther(state, change);
        default:
            throw new Error(`Unknown state: ${state.kind}`);
    }
}

/**
 * @param {ApplicationState} state
 * @param {ImportChange} change
 * @returns {ApplicationState}
 */
function handleImportInInitial(state, change) {
    if (onlyVideoImported(change)) {
        return initialState(change.video);
    }
    const nextVideo = change.video ?? state.video ?? null;
    if (exactlyOneDocumentImported(change)) {
        return otherState(firstImportedDocument(change), nextVideo, true);
    }
    return otherState(null, nextVideo, false);
}

/**
 * @param {ApplicationState} state
 * @param {ImportChange} change
 * @returns {ApplicationState}
 */
function handleImportInOther(state, change) {
    if (state.video !== null && onlyVideoImported(change)) {
        const importedVideo = change.video ?? null;
        if (importedVideo === state.video) {
            return otherState(state.document, state.video, state.saved);
        }
    }
    const nextVideo = change.video ?? state.video ?? null;
    return otherState(null, nextVideo, false);
}
